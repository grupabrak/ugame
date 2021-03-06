# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from settings import GAME_SPEED
from settings import ILOSC_PLANET
from settings import MNOZNIK_MAGAZYNOW
from settings import RES_SPEED

from ..cron_fun import helpers
from ..cron_fun import raporty_fun
from ..funkcje import lock_user_cron


class Output():
    pass


class FleetSurowce():

    def flota_surowce_alien(self, flota, czas_teraz):
        galaktyka_end = flota.galaxy_end
        galaktyka_start = flota.galaxy_start

        req_alien = Output()
        req_alien.user = flota.fleet_owner
        from ..klasy.BaseGame import BaseGame
        GraAlienObj = BaseGame(req_alien, czas_teraz=flota.time - 1, cron=False)

        planeta = self.get_planet(galaktyka_end.planet_id)

        planeta.metal += flota.fleet_resource_metal
        planeta.crystal += flota.fleet_resource_crystal
        planeta.deuter += flota.fleet_resource_deuterium

        raporty_fun.rap_surowce(flota, self)
        raporty_fun.rap_surowce(flota, GraAlienObj)

        GraAlienObj.save_all()


        flota.fleet_resource_metal = 0
        flota.fleet_resource_crystal = 0
        flota.fleet_resource_deuterium = 0

        helpers.make_fleet_back(flota)
        return True



    def flota_surowce(self, flota, czas_teraz):
        galaktyka_end = flota.galaxy_end
        galaktyka_start = flota.galaxy_start


        if not galaktyka_end.planet.owner_id == self.user.pk:
            req_alien = Output()
            req_alien.user = flota.galaxy_end.planet.owner
            from ..klasy.BaseGame import BaseGame
            GraAlienObj = BaseGame(req_alien, czas_teraz=flota.time - 1, cron=False)
            GraAlienObj.cron_function(flota.galaxy_end.planet_id, flota.time - 1)
            planeta = GraAlienObj.get_planet(galaktyka_end.planet_id)
        else:
            planeta = self.get_planet(galaktyka_end.planet_id)

        planeta.metal += flota.fleet_resource_metal
        planeta.crystal += flota.fleet_resource_crystal
        planeta.deuter += flota.fleet_resource_deuterium

        raporty_fun.rap_surowce(flota, self)

        if not planeta.owner_id == self.user.pk:
            raporty_fun.rap_surowce(flota, GraAlienObj)
            GraAlienObj.save_all()

        flota.fleet_resource_metal = 0
        flota.fleet_resource_crystal = 0
        flota.fleet_resource_deuterium = 0

        helpers.make_fleet_back(flota)
        return True
