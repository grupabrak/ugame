# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from math import ceil
from math import sqrt
from string import find
from string import split
from time import localtime
from time import strftime
from time import time

from ugame.models.all import Fleets

from ..cron_fun import helpers
from ..klasy.FleetAtak import FleetAtak
from ..klasy.FleetKolonizuj import FleetKolonizuj
from ..klasy.FleetPowrot import FleetPowrot
from ..klasy.FleetPrzeslij import FleetPrzeslij
from ..klasy.FleetSpy import FleetSpy
from ..klasy.FleetSurowce import FleetSurowce
from ..klasy.FleetZlom import FleetZlom


class Output():pass
class FleetMain(FleetZlom, FleetKolonizuj, FleetSurowce, FleetPrzeslij, FleetAtak, FleetPowrot, FleetSpy):

    def flota_update(self, flota_tmp, czas_teraz):
        flota = Fleets.objects.select_for_update().get(pk=flota_tmp.pk)
        if flota.fleet_owner_id == self.user.id:
            if  flota.fleet_back > 0:
                self.flota_powrot(flota, czas_teraz)
            elif flota.fleet_mission == 1:
                self.fleet_kolonizacja(flota, czas_teraz)
            elif flota.fleet_mission == 2:
                self.flota_surowce(flota, czas_teraz)
            elif flota.fleet_mission == 3:
                self.flota_przeslij(flota, czas_teraz)
            elif flota.fleet_mission == 4:
                self.flota_atak(flota, czas_teraz)
            elif flota.fleet_mission == 5:
                self.fleet_zlom(flota, czas_teraz)
            elif flota.fleet_mission == 6:
                self.flota_spy(flota, czas_teraz)
        else:
            if  flota.fleet_back > 0:
                self.flota_powrot_alien(flota, czas_teraz)
            elif flota.fleet_mission == 1:
                self.fleet_kolonizacja_alien(flota, czas_teraz)
            elif flota.fleet_mission == 2:
                self.flota_surowce_alien(flota, czas_teraz)
            elif flota.fleet_mission == 3:
                self.flota_przeslij_alien(flota, czas_teraz)
            elif flota.fleet_mission == 4:
                self.flota_atak_alien(flota, czas_teraz)
            elif flota.fleet_mission == 5:
                self.fleet_zlom_alien(flota, czas_teraz)
            elif flota.fleet_mission == 6:
                self.flota_spy_alien(flota, czas_teraz)
            # zupenie do przerobki nie dotykamy usera obcego, trzeba stworzyc nowe funkcje ktore operuja na takim czyms
            '''
            self.save_all()
            user_tmp = flota.fleet_owner
            req_alien = Output()
            req_alien.user=flota.fleet_owner
            from game.klasy.BaseGame import BaseGame
            GraAlienObj=BaseGame(req_alien,flota.time)
            GraAlienObj.cron_function(flota.galaxy_end.planet_id,flota.time)
            GraAlienObj.save_all()
            '''
        return True
