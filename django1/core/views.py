from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadFileL5X, UploadFileXml
#from functions import gera_root, tipotag, tagsTela, cruza_tags, intlk, gera_lvu
import lxml.etree as ET
import pandas as pd
import re
from .forms import UploadFileForm
from pandas import DataFrame
from pylogix import PLC
import os
import xml.etree.cElementTree as ETc
from .models import Configuracao, Alarme


"""Padrao_Ain = ["Alm_Fail", "Alm_Hi", "Alm_HiDev", "Alm_HiHi", "Alm_HiRoC", "Alm_Lo", "Alm_LoDev", "Alm_LoLo",
              "Cfg_FailSeverity", "Cfg_HiDevSeverity", "Cfg_HiHiSeverity", "Cfg_HiRoCSeverity", "Cfg_HiSeverity",
              "Cfg_LoDevSeverity", "Cfg_LoLoSeverity", "Cfg_LoSeverity", "Fail.Cfg_MaxShelfT", "Fail.Com_AE.1",
              "Fail.Com_AE.10", "Fail.Com_AE.11", "Fail.Com_AE.4", "Fail.Com_AE.5", "Fail.Com_AE.7",
              "Fail.Com_AE.8", "Hi.Cfg_MaxShelfT", "Hi.Com_AE.1", "Hi.Com_AE.10", "Hi.Com_AE.11", "Hi.Com_AE.4",
              "Hi.Com_AE.5", "Hi.Com_AE.7", "Hi.Com_AE.8", "HiDev.Cfg_MaxShelfT", "HiDev.Com_AE.1",
              "HiDev.Com_AE.10", "HiDev.Com_AE.11", "HiDev.Com_AE.4", "HiDev.Com_AE.5", "HiDev.Com_AE.7",
              "HiDev.Com_AE.8", "HiHi.Cfg_MaxShelfT", "HiHi.Com_AE.1", "HiHi.Com_AE.10", "HiHi.Com_AE.11",
              "HiHi.Com_AE.4", "HiHi.Com_AE.5", "HiHi.Com_AE.7", "HiHi.Com_AE.8", "HiRoC.Cfg_MaxShelfT",
              "HiRoC.Com_AE.1", "HiRoC.Com_AE.10", "HiRoC.Com_AE.11", "HiRoC.Com_AE.4", "HiRoC.Com_AE.5",
              "HiRoC.Com_AE.7", "HiRoC.Com_AE.8", "Lo.Cfg_MaxShelfT", "Lo.Com_AE.1", "Lo.Com_AE.10", "Lo.Com_AE.11",
              "Lo.Com_AE.4", "Lo.Com_AE.5", "Lo.Com_AE.7", "Lo.Com_AE.8", "LoDev.Cfg_MaxShelfT", "LoDev.Com_AE.1",
              "LoDev.Com_AE.10", "LoDev.Com_AE.11", "LoDev.Com_AE.4", "LoDev.Com_AE.5", "LoDev.Com_AE.7",
              "LoDev.Com_AE.8", "LoLo.Cfg_MaxShelfT", "LoLo.Com_AE.1", "LoLo.Com_AE.10", "LoLo.Com_AE.11",
              "LoLo.Com_AE.4", "LoLo.Com_AE.5", "LoLo.Com_AE.7", "LoLo.Com_AE.8", "Val", "Val_Dev", "Val_InpPV",
              "Val_RoC"]
Padrao_Din = ["Alm_IOFault", "Alm_TgtDisagree", "Alm_TgtDisagreeW", "Cfg_IOFaultSeverity",
              "Cfg_TgtDisagreeSeverity", "Cfg_TgtDisagreeWSeverity", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
              "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7",
              "IOFault.Com_AE.8", "Inp_PV", "Inp_Target", "TgtDisagree.Cfg_MaxShelfT", "TgtDisagree.Com_AE.1",
              "TgtDisagree.Com_AE.10", "TgtDisagree.Com_AE.11", "TgtDisagree.Com_AE.4", "TgtDisagree.Com_AE.5",
              "TgtDisagree.Com_AE.7", "TgtDisagree.Com_AE.8", "TgtDisagreeW.Cfg_MaxShelfT", "TgtDisagreeW.Com_AE.1",
              "TgtDisagreeW.Com_AE.10", "TgtDisagreeW.Com_AE.11", "TgtDisagreeW.Com_AE.4", "TgtDisagreeW.Com_AE.5",
              "TgtDisagreeW.Com_AE.7", "TgtDisagreeW.Com_AE.8"]
Padrao_VSD = ["Alm_DriveFault", "Alm_FailToStart", "Alm_FailToStop", "Alm_IOFault", "Alm_IntlkTrip",
              "Cfg_DriveFaultSeverity", "Cfg_FailToStartSeverity", "Cfg_FailToStopSeverity", "Cfg_IOFaultSeverity",
              "Cfg_IntlkTripSeverity", "DriveFault.Cfg_MaxShelfT", "DriveFault.Com_AE.1", "DriveFault.Com_AE.10",
              "DriveFault.Com_AE.11", "DriveFault.Com_AE.4", "DriveFault.Com_AE.5", "DriveFault.Com_AE.7",
              "DriveFault.Com_AE.8", "FailToStart.Cfg_MaxShelfT", "FailToStart.Com_AE.1", "FailToStart.Com_AE.10",
              "FailToStart.Com_AE.11", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5", "FailToStart.Com_AE.7",
              "FailToStart.Com_AE.8", "FailToStop.Cfg_MaxShelfT", "FailToStop.Com_AE.1", "FailToStop.Com_AE.10",
              "FailToStop.Com_AE.11", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5", "FailToStop.Com_AE.7",
              "FailToStop.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10",
              "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8",
              "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11",
              "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8"]
Padrao_Motor = ["Alm_FailToStart", "FailToStart.Com_AE.9", "FailToStart.Com_AE.1", "FailToStart.Com_AE.6",
                "FailToStart.Com_AE.3", "FailToStart.Com_AE.10", "FailToStart.Com_AE.11", "FailToStart.Com_AE.7",
                "FailToStart.Com_AE.8", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5", "FailToStart.Cfg_MaxShelfT",
                "Cfg_FailToStartSeverity", "Alm_FailToStop", "FailToStop.Com_AE.9", "FailToStop.Com_AE.1",
                "FailToStop.Com_AE.6", "FailToStop.Com_AE.3", "FailToStop.Com_AE.10", "FailToStop.Com_AE.11",
                "FailToStop.Com_AE.7", "FailToStop.Com_AE.8", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5",
                "FailToStop.Cfg_MaxShelfT", "Cfg_FailToStopSeverity", "Alm_IntlkTrip", "IntlkTrip.Com_AE.9",
                "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.6", "IntlkTrip.Com_AE.3", "IntlkTrip.Com_AE.10",
                "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "IntlkTrip.Com_AE.4",
                "IntlkTrip.Com_AE.5", "IntlkTrip.Cfg_MaxShelfT", "Cfg_IntlkTripSeverity", "Alm_IOFault",
                "IOFault.Com_AE.9", "IOFault.Com_AE.1", "IOFault.Com_AE.6", "IOFault.Com_AE.3", "IOFault.Com_AE.10",
                "IOFault.Com_AE.11", "IOFault.Com_AE.7", "IOFault.Com_AE.8", "IOFault.Com_AE.4", "IOFault.Com_AE.5",
                "IOFault.Cfg_MaxShelfT", "Cfg_IOFaultSeverity"]
Padrao_ValveSO = ["Alm_IntlkTrip", "Cfg_IntlkTripSeverity", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1",
                  "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5",
                  "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "Alm_FullStall", "Alm_IOFault", "Alm_IntlkTrip",
                  "Alm_TransitStall", "Cfg_FullStallSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
                  "Cfg_TransitStallSeverity", "FullStall.Cfg_MaxShelfT", "FullStall.Com_AE.1",
                  "FullStall.Com_AE.10", "FullStall.Com_AE.11", "FullStall.Com_AE.4", "FullStall.Com_AE.5",
                  "FullStall.Com_AE.7", "FullStall.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
                  "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5",
                  "IOFault.Com_AE.7", "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1",
                  "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5",
                  "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "TransitStall.Cfg_MaxShelfT", "TransitStall.Com_AE.1",
                  "TransitStall.Com_AE.10", "TransitStall.Com_AE.11", "TransitStall.Com_AE.4",
                  "TransitStall.Com_AE.5", "TransitStall.Com_AE.7", "TransitStall.Com_AE.8"]
Padrao_ValveC = ["ActuatorFault.Cfg_MaxShelfT", "ActuatorFault.Com_AE.1", "ActuatorFault.Com_AE.10",
                 "ActuatorFault.Com_AE.11", "ActuatorFault.Com_AE.4", "ActuatorFault.Com_AE.5",
                 "ActuatorFault.Com_AE.7", "ActuatorFault.Com_AE.8", "Alm_ActuatorFault", "Alm_FullStall",
                 "Alm_IOFault", "Alm_IntlkTrip", "Alm_TransitStall", "Cfg_ActuatorFaultSeverity",
                 "Cfg_FullStallSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
                 "Cfg_TransitStallSeverity", "FullStall.Cfg_MaxShelfT", "FullStall.Com_AE.1", "FullStall.Com_AE.10",
                 "FullStall.Com_AE.11", "FullStall.Com_AE.4", "FullStall.Com_AE.5", "FullStall.Com_AE.7",
                 "FullStall.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10",
                 "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7",
                 "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10",
                 "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7",
                 "IntlkTrip.Com_AE.8", "TransitStall.Cfg_MaxShelfT", "TransitStall.Com_AE.1",
                 "TransitStall.Com_AE.10", "TransitStall.Com_AE.11", "TransitStall.Com_AE.4",
                 "TransitStall.Com_AE.5", "TransitStall.Com_AE.7", "TransitStall.Com_AE.8", "Val_Fault"]
Padrao_Dout = ["Alm_IntlkTrip", "IntlkTrip.Com_AE.9", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.6",
               "IntlkTrip.Com_AE.3", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.7",
               "IntlkTrip.Com_AE.8", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Cfg_MaxShelfT",
               "Cfg_IntlkTripSeverity", "Alm_IOFault", "IOFault.Com_AE.9", "IOFault.Com_AE.1", "IOFault.Com_AE.6",
               "IOFault.Com_AE.3", "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.7", "IOFault.Com_AE.8",
               "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Cfg_MaxShelfT", "Cfg_IOFaultSeverity",
               "Alm_OffFail", "Val_Cmd", "Val_Fdbk", "OffFail.Com_AE.9", "OffFail.Com_AE.1", "OffFail.Com_AE.6",
               "OffFail.Com_AE.3", "OffFail.Com_AE.10", "OffFail.Com_AE.11", "OffFail.Com_AE.7", "OffFail.Com_AE.8",
               "OffFail.Com_AE.4", "OffFail.Com_AE.5", "OffFail.Cfg_MaxShelfT", "Cfg_OffFailSeverity", "Alm_OnFail",
               "OnFail.Com_AE.9", "OnFail.Com_AE.1", "OnFail.Com_AE.6", "OnFail.Com_AE.3", "OnFail.Com_AE.10",
               "OnFail.Com_AE.11", "OnFail.Com_AE.7", "OnFail.Com_AE.8", "OnFail.Com_AE.4", "OnFail.Com_AE.5",
               "OnFail.Cfg_MaxShelfT", "Cfg_OnFailSeverity"]
Padrao_Seq = ["Alm_StepTO", "Val_CurrStepNum", "StepTO.Com_AE.9", "StepTO.Com_AE.1", "StepTO.Com_AE.6",
              "StepTO.Com_AE.3", "StepTO.Com_AE.10", "StepTO.Com_AE.11", "StepTO.Com_AE.7", "StepTO.Com_AE.8",
              "StepTO.Com_AE.4", "StepTO.Com_AE.5", "StepTO.Cfg_MaxShelfT", "Cfg_SeqTOSeverity", "Alm_SeqTO",
              "SeqTO.Com_AE.9", "SeqTO.Com_AE.1", "SeqTO.Com_AE.6", "SeqTO.Com_AE.3", "SeqTO.Com_AE.10",
              "SeqTO.Com_AE.11", "SeqTO.Com_AE.7", "SeqTO.Com_AE.8", "SeqTO.Com_AE.4", "SeqTO.Com_AE.5",
              "SeqTO.Cfg_MaxShelfT", "Cfg_StepTOSeverity", "Alm_IntlkTrip", "IntlkTrip.Com_AE.9",
              "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.6", "IntlkTrip.Com_AE.3", "IntlkTrip.Com_AE.10",
              "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "IntlkTrip.Com_AE.4",
              "IntlkTrip.Com_AE.5", "IntlkTrip.Cfg_MaxShelfT", "Cfg_IntlkTripSeverity"]
Padrao_D4SD = ["Alm_FailToStart", "Alm_FailToStop", "Alm_IOFault", "Alm_IntlkTrip", "Cfg_FailToStartSeverity",
               "Cfg_FailToStopSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
               "FailToStart.Cfg_MaxShelfT", "FailToStart.Com_AE.1", "FailToStart.Com_AE.10",
               "FailToStart.Com_AE.11", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5", "FailToStart.Com_AE.7",
               "FailToStart.Com_AE.8", "FailToStop.Cfg_MaxShelfT", "FailToStop.Com_AE.1", "FailToStop.Com_AE.10",
               "FailToStop.Com_AE.11", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5", "FailToStop.Com_AE.7",
               "FailToStop.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10",
               "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8",
               "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11",
               "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8",
               "Alm_IOFault", "Alm_Trip", "Alm_Warn", "Cfg_IOFaultSeverity", "Cfg_TripSeverity", "Cfg_WarnSeverity",
               "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10", "IOFault.Com_AE.11",
               "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8", "Trip.Cfg_MaxShelfT",
               "Trip.Com_AE.1", "Trip.Com_AE.10", "Trip.Com_AE.11", "Trip.Com_AE.4", "Trip.Com_AE.5",
               "Trip.Com_AE.7", "Trip.Com_AE.8", "Val_TripCode", "Val_WarningCode", "Warn.Cfg_MaxShelfT",
               "Warn.Com_AE.1", "Warn.Com_AE.10", "Warn.Com_AE.11", "Warn.Com_AE.4", "Warn.Com_AE.5",
               "Warn.Com_AE.7", "Warn.Com_AE.8", "", "", "", "", "", "", "Alm_FailToStart", "Alm_FailToStop",
               "Alm_IOFault", "Alm_IntlkTrip", "Cfg_FailToStartSeverity", "Cfg_FailToStopSeverity",
               "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity", "FailToStart.Cfg_MaxShelfT", "FailToStart.Com_AE.1",
               "FailToStart.Com_AE.10", "FailToStart.Com_AE.11", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5",
               "FailToStart.Com_AE.7", "FailToStart.Com_AE.8", "FailToStop.Cfg_MaxShelfT", "FailToStop.Com_AE.1",
               "FailToStop.Com_AE.10", "FailToStop.Com_AE.11", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5",
               "FailToStop.Com_AE.7", "FailToStop.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
               "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7",
               "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10",
               "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7",
               "IntlkTrip.Com_AE.8", "", "", "", "", "", "", "", "Alm_CantStart", "Alm_CantStop", "Alm_IntlkTrip",
               "CantStart.Cfg_MaxShelfT", "CantStart.Com_AE.1", "CantStart.Com_AE.10", "CantStart.Com_AE.11",
               "CantStart.Com_AE.4", "CantStart.Com_AE.5", "CantStart.Com_AE.7", "CantStart.Com_AE.8",
               "CantStop.Cfg_MaxShelfT", "CantStop.Com_AE.1", "CantStop.Com_AE.10", "CantStop.Com_AE.11",
               "CantStop.Com_AE.4", "CantStop.Com_AE.5", "CantStop.Com_AE.7", "CantStop.Com_AE.8",
               "Cfg_CantStartSeverity", "Cfg_CantStopSeverity", "Cfg_IntlkTripSeverity", "IntlkTrip.Cfg_MaxShelfT",
               "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4",
               "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "Val_Cmd", "Val_Fdbk", "", "", "",
               "", "", "", "", "ActuatorFault.Cfg_MaxShelfT", "ActuatorFault.Com_AE.1", "ActuatorFault.Com_AE.10",
               "ActuatorFault.Com_AE.11", "ActuatorFault.Com_AE.4", "ActuatorFault.Com_AE.5",
               "ActuatorFault.Com_AE.7", "ActuatorFault.Com_AE.8", "Alm_ActuatorFault", "Alm_FullStall",
               "Alm_IOFault", "Alm_IntlkTrip", "Alm_TransitStall", "Cfg_ActuatorFaultSeverity",
               "Cfg_FullStallSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity", "Cfg_TransitStallSeverity",
               "FullStall.Cfg_MaxShelfT", "FullStall.Com_AE.1", "FullStall.Com_AE.10", "FullStall.Com_AE.11",
               "FullStall.Com_AE.4", "FullStall.Com_AE.5", "FullStall.Com_AE.7", "FullStall.Com_AE.8",
               "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10", "IOFault.Com_AE.11",
               "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8",
               "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11",
               "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8",
               "TransitStall.Cfg_MaxShelfT", "TransitStall.Com_AE.1", "TransitStall.Com_AE.10",
               "TransitStall.Com_AE.11", "TransitStall.Com_AE.4", "TransitStall.Com_AE.5", "TransitStall.Com_AE.7",
               "TransitStall.Com_AE.8", "Val_Fault"]
Padrao_E300Ovld = ["Alm_FailToStart", "Alm_FailToStop", "Alm_IOFault", "Alm_IntlkTrip", "Cfg_FailToStartSeverity",
                   "Cfg_FailToStopSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
                   "FailToStart.Cfg_MaxShelfT", "FailToStart.Com_AE.1", "FailToStart.Com_AE.10",
                   "FailToStart.Com_AE.11", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5", "FailToStart.Com_AE.7",
                   "FailToStart.Com_AE.8", "FailToStop.Cfg_MaxShelfT", "FailToStop.Com_AE.1",
                   "FailToStop.Com_AE.10", "FailToStop.Com_AE.11", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5",
                   "FailToStop.Com_AE.7", "FailToStop.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
                   "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5",
                   "IOFault.Com_AE.7", "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1",
                   "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5",
                   "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "Alm_IOFault", "Alm_Trip", "Alm_Warn",
                   "Cfg_IOFaultSeverity", "Cfg_TripSeverity", "Cfg_WarnSeverity", "IOFault.Cfg_MaxShelfT",
                   "IOFault.Com_AE.1", "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4",
                   "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8", "Trip.Cfg_MaxShelfT",
                   "Trip.Com_AE.1", "Trip.Com_AE.10", "Trip.Com_AE.11", "Trip.Com_AE.4", "Trip.Com_AE.5",
                   "Trip.Com_AE.7", "Trip.Com_AE.8", "Val_TripCode", "Val_WarningCode", "Warn.Cfg_MaxShelfT",
                   "Warn.Com_AE.1", "Warn.Com_AE.10", "Warn.Com_AE.11", "Warn.Com_AE.4", "Warn.Com_AE.5",
                   "Warn.Com_AE.7", "Warn.Com_AE.8"]
Padrao_MotorRev = ["Alm_FailToStart", "Alm_FailToStop", "Alm_IOFault", "Alm_IntlkTrip", "Cfg_FailToStartSeverity",
                   "Cfg_FailToStopSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
                   "FailToStart.Cfg_MaxShelfT", "FailToStart.Com_AE.1", "FailToStart.Com_AE.10",
                   "FailToStart.Com_AE.11", "FailToStart.Com_AE.4", "FailToStart.Com_AE.5", "FailToStart.Com_AE.7",
                   "FailToStart.Com_AE.8", "FailToStop.Cfg_MaxShelfT", "FailToStop.Com_AE.1",
                   "FailToStop.Com_AE.10", "FailToStop.Com_AE.11", "FailToStop.Com_AE.4", "FailToStop.Com_AE.5",
                   "FailToStop.Com_AE.7", "FailToStop.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
                   "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5",
                   "IOFault.Com_AE.7", "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1",
                   "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5",
                   "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8"]
Padrao_LLS = ["Alm_CantStart", "Alm_CantStop", "Alm_IntlkTrip", "CantStart.Cfg_MaxShelfT", "CantStart.Com_AE.1",
              "CantStart.Com_AE.10", "CantStart.Com_AE.11", "CantStart.Com_AE.4", "CantStart.Com_AE.5",
              "CantStart.Com_AE.7", "CantStart.Com_AE.8", "CantStop.Cfg_MaxShelfT", "CantStop.Com_AE.1",
              "CantStop.Com_AE.10", "CantStop.Com_AE.11", "CantStop.Com_AE.4", "CantStop.Com_AE.5",
              "CantStop.Com_AE.7", "CantStop.Com_AE.8", "Cfg_CantStartSeverity", "Cfg_CantStopSeverity",
              "Cfg_IntlkTripSeverity", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10",
              "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7",
              "IntlkTrip.Com_AE.8", "Val_Cmd", "Val_Fdbk"]
Padrao_ValveMO = ["ActuatorFault.Cfg_MaxShelfT", "ActuatorFault.Com_AE.1", "ActuatorFault.Com_AE.10",
                  "ActuatorFault.Com_AE.11", "ActuatorFault.Com_AE.4", "ActuatorFault.Com_AE.5",
                  "ActuatorFault.Com_AE.7", "ActuatorFault.Com_AE.8", "Alm_ActuatorFault", "Alm_FullStall",
                  "Alm_IOFault", "Alm_IntlkTrip", "Alm_TransitStall", "Cfg_ActuatorFaultSeverity",
                  "Cfg_FullStallSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity",
                  "Cfg_TransitStallSeverity", "FullStall.Cfg_MaxShelfT", "FullStall.Com_AE.1",
                  "FullStall.Com_AE.10", "FullStall.Com_AE.11", "FullStall.Com_AE.4", "FullStall.Com_AE.5",
                  "FullStall.Com_AE.7", "FullStall.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1",
                  "IOFault.Com_AE.10", "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5",
                  "IOFault.Com_AE.7", "IOFault.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1",
                  "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5",
                  "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "TransitStall.Cfg_MaxShelfT", "TransitStall.Com_AE.1",
                  "TransitStall.Com_AE.10", "TransitStall.Com_AE.11", "TransitStall.Com_AE.4",
                  "TransitStall.Com_AE.5", "TransitStall.Com_AE.7", "TransitStall.Com_AE.8", "Val_Fault"]
Padrao_D4SD = ["Alm_DeviceFault", "Alm_Fail", "Alm_IOFault", "Alm_IntlkTrip", "Cfg_DeviceFaultSeverity",
               "Cfg_FailSeverity", "Cfg_IOFaultSeverity", "Cfg_IntlkTripSeverity", "DeviceFault.Cfg_MaxShelfT",
               "DeviceFault.Com_AE.1", "DeviceFault.Com_AE.10", "DeviceFault.Com_AE.11", "DeviceFault.Com_AE.4",
               "DeviceFault.Com_AE.5", "DeviceFault.Com_AE.7", "DeviceFault.Com_AE.8", "Fail.Cfg_MaxShelfT",
               "Fail.Com_AE.1", "Fail.Com_AE.10", "Fail.Com_AE.11", "Fail.Com_AE.4", "Fail.Com_AE.5",
               "Fail.Com_AE.7", "Fail.Com_AE.8", "IOFault.Cfg_MaxShelfT", "IOFault.Com_AE.1", "IOFault.Com_AE.10",
               "IOFault.Com_AE.11", "IOFault.Com_AE.4", "IOFault.Com_AE.5", "IOFault.Com_AE.7", "IOFault.Com_AE.8",
               "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10", "IntlkTrip.Com_AE.11",
               "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7", "IntlkTrip.Com_AE.8", "Val_Cmd",
               "Val_Sts", "Val_FirstOutTxt"]
Padrao_PIDE = ["Alm_Fail", "Alm_HiDev", "Alm_HiHiDev", "Alm_IntlkTrip", "Alm_LoDev", "Alm_LoLoDev",
               "Cfg_FailSeverity", "Cfg_HiDevSeverity", "Cfg_HiHiDevSeverity", "Cfg_IntlkTripSeverity",
               "Cfg_LoDevSeverity", "Cfg_LoLoDevSeverity", "Fail.Cfg_MaxShelfT", "Fail.Com_AE.1", "Fail.Com_AE.10",
               "Fail.Com_AE.11", "Fail.Com_AE.4", "Fail.Com_AE.5", "Fail.Com_AE.7", "Fail.Com_AE.8",
               "HiDev.Cfg_MaxShelfT", "HiDev.Com_AE.1", "HiDev.Com_AE.10", "HiDev.Com_AE.11", "HiDev.Com_AE.4",
               "HiDev.Com_AE.5", "HiDev.Com_AE.7", "HiDev.Com_AE.8", "HiHiDev.Cfg_MaxShelfT", "HiHiDev.Com_AE.1",
               "HiHiDev.Com_AE.10", "HiHiDev.Com_AE.11", "HiHiDev.Com_AE.4", "HiHiDev.Com_AE.5", "HiHiDev.Com_AE.7",
               "HiHiDev.Com_AE.8", "IntlkTrip.Cfg_MaxShelfT", "IntlkTrip.Com_AE.1", "IntlkTrip.Com_AE.10",
               "IntlkTrip.Com_AE.11", "IntlkTrip.Com_AE.4", "IntlkTrip.Com_AE.5", "IntlkTrip.Com_AE.7",
               "IntlkTrip.Com_AE.8", "LoDev.Cfg_MaxShelfT", "LoDev.Com_AE.1", "LoDev.Com_AE.10", "LoDev.Com_AE.11",
               "LoDev.Com_AE.4", "LoDev.Com_AE.5", "LoDev.Com_AE.7", "LoDev.Com_AE.8", "LoLoDev.Cfg_MaxShelfT",
               "LoLoDev.Com_AE.1", "LoLoDev.Com_AE.10", "LoLoDev.Com_AE.11", "LoLoDev.Com_AE.4", "LoLoDev.Com_AE.5",
               "LoLoDev.Com_AE.7", "LoLoDev.Com_AE.8", "Val_Fault", "Val_PV", "Val_SP"]
#Padrão Tags Alarme
Padrao_Alm_Ain = ["Alm_LoLo", "Alm_LoDev", "Alm_Lo", "Alm_HiRoC", "Alm_HiHi", "Alm_HiDev", "Alm_Hi", "Alm_Fail"]
Padrao_Alm_Din = ["Alm_TgtDisagreeW", "Alm_TgtDisagree", "Alm_IOFault"]
Padrao_Alm_Dout = ["Alm_OnFail", "Alm_OffFail", "Alm_IOFault", "Alm_IntlkTrip"]
Padrao_Alm_E300 = ["Alm_Warn", "Alm_Trip", "Alm_IOFault"]
Padrao_Alm_E3 = ["Alm_Warn", "Alm_Trip", "Alm_IOFault"]
Padrao_Alm_LLS = ["Alm_IntlkTrip", "Alm_CantStop", "Alm_CantStart"]
Padrao_Alm_Motor = ["Alm_IOFault", "Alm_IntlkTrip", "Alm_FailToStop", "Alm_FailToStart"]
Padrao_Alm_MotorRev = ["Alm_IOFault", "Alm_IntlkTrip", "Alm_FailToStop", "Alm_FailToStart"]
Padrao_Alm_PF = ["Alm_IOFault", "Alm_IntlkTrip", "Alm_FailToStop", "Alm_FailToStart", "Alm_DriveFault"]
Padrao_Alm_PIDE = ["Alm_LoLoDev", "Alm_LoDev", "Alm_IntlkTrip", "Alm_HiHiDev", "Alm_HiDev", "Alm_Fail"]
Padrao_Alm_VSD = ["Alm_IOFault", "Alm_IntlkTrip", "Alm_FailToStop", "Alm_FailToStart", "Alm_DriveFault"]
Padrao_Alm_D4SD = ["Alm_DeviceFault", "Alm_Fail", "Alm_IntlkTrip", "Alm_IOFault"]
Padrao_Alm_P_Seq = ["Alm_IntlkTrip", "Alm_SeqTO", "Alm_StepTO"]
Padrao_Alm_ValveC = ["Alm_IOFault", "Alm_IntlkTrip", "Alm_ActuatorFault"]
Padrao_Alm_ValveMO = ["Alm_TransitStall", "Alm_IOFault", "Alm_IntlkTrip", "Alm_FullStall", "Alm_ActuatorFault"]
Padrao_Alm_ValveSO = ["Alm_FullStall", "Alm_IntlkTrip", "Alm_IOFault", "Alm_TransitStall"] """


aux = []
lista_alarmes = []
c = Alarme.objects.filter(alarme_objeto__nome= 'Padrao_Ain')
teste = Configuracao.objects.filter(alarme__alarme_objeto__nome= 'Padrao_Ain')
for alarme in lista_alarmes:
    lista_alarmes.append(alarme.nome)
for item in c:
    aux.append(item.nome)
for item in teste:
    obj = [item.severity, item.input_tag]
    aux = aux + obj



Padrao_Msg_Text = {
    "P_Din": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG", "", "", ""],
        "Alm_TgtDisagree": [
            "Alarme Atuado: DESCRIÇÃO_DA_TAG PV Diferente do Target;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/; ",
            ".Inp_PV", ".Inp_Target", ""],
        "Alm_TgtDisagreeW": [
            "Aviso: DESCRIÇÃO_DA_TAG PV Diferente do Target ;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/; ",
            ".Inp_PV", ".Inp_Target", ""]
    },

    "P_DinAdv": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG", "", "", ""],
        "Alm_TgtDisagree": [
            "Alarme Atuado: DESCRIÇÃO_DA_TAG PV Diferente do Target;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/; ",
            ".Inp_PV", ".Inp_Target", ""],
        "Alm_TgtDisagreeW": [
            "Aviso: DESCRIÇÃO_DA_TAG PV Diferente do Target ;  Inp_PV=/*S:0%Tag1*/;  Inp_Target=/*S:0%Tag2*/; ",
            ".Inp_PV", ".Inp_Target", ""]
    },

    "P_Ain": {
        "Alm_LoLo": ["DESCRIÇÃO_DA_TAG Alarme Muito Baixo.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_LoDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Baixo.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/", ".Val_PV",
                      ".Val_SP", ""],
        "Alm_Lo": ["DESCRIÇÃO_DA_TAG Alarme  Baixo.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_HiRoC": ["DESCRIÇÃO_DA_TAG Alarme de Taxa de Mudança Alta.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "",
                      ""],
        "Alm_HiHi": ["DESCRIÇÃO_DA_TAG Alarme Muito Alto.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_HiDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Alto.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/", ".Val_PV",
                      ".Val_SP", ""],
        "Alm_Hi": ["DESCRIÇÃO_DA_TAG Alarme  Alto.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_Fail": [
            "DESCRIÇÃO_DA_TAG  PV Ruim ou Fora de Alcance ;  Val=/*N:5 %Tag1 NOFILL DP:1*/; Val_InpPV=/*N:5 %Tag2 NOFILL DP:1*/; ",
            ".Val", ".Val_InpPV", ""]
    },

    "P_AinAdv": {
        "Alm_LoLo": ["DESCRIÇÃO_DA_TAG Alarme Muito Baixo.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_LoDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Baixo.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/", ".Val_PV",
                      ".Val_SP", ""],
        "Alm_Lo": ["DESCRIÇÃO_DA_TAG Alarme  Baixo.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_HiRoC": ["DESCRIÇÃO_DA_TAG Alarme de Taxa de Mudança Alta.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "",
                      ""],
        "Alm_HiHi": ["DESCRIÇÃO_DA_TAG Alarme Muito Alto.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_HiDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Alto.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/", ".Val_PV",
                      ".Val_SP", ""],
        "Alm_Hi": ["DESCRIÇÃO_DA_TAG Alarme  Alto.   Val=/*N:5 %Tag1 NOFILL DP:1*/; ", ".Val", "", ""],
        "Alm_Fail": [
            "DESCRIÇÃO_DA_TAG  PV Ruim ou Fora de Alcance ;  Val=/*N:5 %Tag1 NOFILL DP:1*/; Val_InpPV=/*N:5 %Tag2 NOFILL DP:1*/; ",
            ".Val", ".Val_InpPV", ""]
    },

    "P_Dout": {
        "Alm_OnFail": [
            "DESCRIÇÃO_DA_TAG O feedback do dispositivo não confirma que o dispositivo está LIGADO dentro do tempo configurado. Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/; ",
            ".Val_Cmd", ".Val_Fdbk", ""],
        "Alm_OffFail": [
            "DESCRIÇÃO_DA_TAG O feedback do dispositivo não confirma que o dispositivo está DESLIGADO dentro do tempo configurado. Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/; ",
            ".Val_Cmd", ".Val_Fdbk", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""]
    },

    "P_E300Ovld": {
        "Alm_Warn": ["DESCRIÇÃO_DA_TAG Aviso iminente de falha.   Val_WarningCode=/*S:0%Tag1*/; ",
                     "_Ovld.Val_WarningCode", "", ""],
        "Alm_Trip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "_Ovld.Val_TripCode", "", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG", "", "", ""]
    },

    "P_E3Ovld": {
        "Alm_Warn": ["DESCRIÇÃO_DA_TAG Aviso iminente de falha.   Val_WarningCode=/*S:0%Tag1*/; ",
                     "_Ovld.Val_WarningCode", "", ""],
        "Alm_Trip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "_Ovld.Val_TripCode", "", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG", "", "", ""]
    },

    "P_LLS": {
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "_Intlk.Val_FirstOutTxt", "", ""],
        "Alm_CantStop": ["DESCRIÇÃO_DA_TAG Falha paraParar.   Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;", ".Val_Cmd",
                         ".Val_Fdbk", ""],
        "Alm_CantStart": ["DESCRIÇÃO_DA_TAG Falha para Partir.   Val_Cmd=/*S:0%Tag1*/; Val_Fdbk=/*S:0%Tag2*/;",
                          ".Val_Cmd", ".Val_Fdbk", ""]
    },

    "P_Motor": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_FailToStop": ["Falha Para Parar DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_FailToStart": ["Falha Para Partir DESCRIÇÃO_DA_TAG ", "", "", ""]
    },

    "P_MotorRev": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_FailToStop": ["Falha Para Parar DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_FailToStart": ["Falha Para Partir DESCRIÇÃO_DA_TAG ", "", "", ""]
    },

    "P_PIDE": {
        "Alm_LoLoDev": ["DESCRIÇÃO_DA_TAG . Alarme de Desvio Muito Baixo.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;",
                        ".Val_PV", ".Val_SP", ""],
        "Alm_LoDev": ["DESCRIÇÃO_DA_TAG . Alarme de Desvio  Baixo.   Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/;",
                      ".Val_PV", ".Val_SP", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "_Intlk.Val_FirstOutTxt", "", ""],
        "Alm_HiHiDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Muito Alto.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/",
                        ".Val_PV", ".Val_SP", ""],
        "Alm_HiDev": ["DESCRIÇÃO_DA_TAG Alarme de Desvio Alto.  Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/", ".Val_PV",
                      ".Val_SP", ""],
        "Alm_Fail": [
            "DESCRIÇÃO_DA_TAG a Instrução Possui uma Falha. Val_PV=/*S:0%Tag1*/; Val_SP=/*S:0%Tag2*/; Val_Fault=/*S:0%Tag3*/;",
            ".Val_PV", ".Val_SP", ".Val_Fault"]
    },

    "P_VSD": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_FailToStop": ["Falha Para Parar DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_FailToStart": ["Falha Para Partir DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_DriveFault": ["DESCRIÇÃO_DA_TAG Falha de Acionamento.  Val_Fault=/*S:0%Tag1*/", ".Val_Fault", "", ""]
    },

    "P_PF755": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "_Intlk.Val_FirstOutTxt", "", ""],
        "Alm_FailToStop": ["Falha Para Parar DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_FailToStart": ["Falha Para Partir DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_DriveFault": ["DESCRIÇÃO_DA_TAG Falha de Acionamento.  Val_Fault=/*S:0%Tag1*/", ".Val_Fault", "", ""]
    },

    "P_D4SD": {
        "Alm_DeviceFault": ["DESCRIÇÃO_DA_TAG Falha de Acionamento.  Val_Fault=/*S:0%Tag1*/", ".Val_Fault", "", ""],
        "Alm_Fail": [
            "DESCRIÇÃO_DA_TAG  O dispositivo não conseguiu alcançar a posição comandada.  Val_Cmd=/*S:0%Tag1*/; Val_Sts=/*S:0%Tag2*/;",
            ".Val_Cmd", ".Val_Sts", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""]
    },

    "P_Seq": {
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_SeqTO": ["DESCRIÇÃO_DA_TAG  Alarme de Tempo Limite de Sequencia", "", "", ""],
        "Alm_StepTO": ["DESCRIÇÃO_DA_TAG  Alarme de Tempo Limite de Etapa.  Val_CurrStepNum=/*S:0%Tag1*/",
                       ".Val_CurrStepNum", "", ""]
    },

    "P_ValveC": {
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_ActuatorFault": ["DESCRIÇÃO_DA_TAG Falha do Atuador.  Val_Fault=/*S:0%Tag1*/;", ".Val_Fault", "", ""]
    },

    "P_ValveMO": {
        "Alm_TransitStall": ["DESCRIÇÃO_DA_TAG Movimentação Impedida - a Válvula não se Moveu Para a Posição Alvo", "",
                             "", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_FullStall": ["DESCRIÇÃO_DA_TAG Parada Total - a Válvula Não se Moveu", "", "", ""],
        "Alm_ActuatorFault": ["DESCRIÇÃO_DA_TAG Falha do Atuador.  Val_Fault=/*S:0%Tag1*/;", ".Val_Fault", "", ""]
    },
    "P_ValveSO": {
        "Alm_FullStall": ["DESCRIÇÃO_DA_TAG Parada Total - a Válvula Não se Moveu", "", "", ""],
        "Alm_IntlkTrip": ["DESCRIÇÃO_DA_TAG Intertravamento: /*S:0%Tag1*/;", "", "", ""],
        "Alm_IOFault": ["Falha I/O: DESCRIÇÃO_DA_TAG ", "", "", ""],
        "Alm_TransitStall": ["DESCRIÇÃO_DA_TAG Movimentação Impedida - a Válvula não se Moveu Para a Posição Alvo", "",
                             "", ""]
    }
}
# Funções do Interlock
def ledados(tag):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        valor = comm.Read(tag)
        return valor.Value

def lestring(tag):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        str_len = comm.Read(tag + '.LEN').Value
        if str_len > 0:
            data = comm.Read(tag + '.DATA[0]', int(str_len)).Value
            value = ''.join([chr(d) for d in data])
        else:
            value = ' '
        ret = value
        # print(value)


def escrevestring(TAG, txt):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        stuff = [ord(c) for c in txt]
        comm.Write(TAG + '.LEN', len(stuff))
        comm.Write(TAG + '.DATA[0]', stuff)


def escreve(TAG, valor):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        comm.Write(TAG, valor)


def inserir_linha(idx, df, df_inserir):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]

    df = dfA.append(df_inserir).append(dfB).reset_index(drop=True)

    return df


def tipotag(tag, root):
    # Acha todas as rotinas do tipo Function Block Diagram (FBD)
    for elem in root.findall(".//Tags/Tag[@Name='" + tag + "']"):
        return elem.attrib['DataType']

def tagdesc(tag,root):
    # Acha a descrição das tags
    for elem in root.findall(".//Tags/Tag[@Name='"+tag+"']/Description/LocalizedDescription"):
        texto=elem.text
        if isinstance(texto,str):
            return texto
        else:
            return " "


def tagsTela(xml_teste):
    ##print(xml_teste, type(xml_teste))
    #settings_dir = os.path.dirname(__file__)
    #PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    #TELAS_FOLDER = os.path.join(PROJECT_ROOT, 'Telas/')
    #telas = os.listdir(TELAS_FOLDER)
    print('xml teste de tagsTela', xml_teste)
    telas = xml_teste
    #print('xml_teste -----', xml_teste)
    print ('telas-----', telas)
    telasname = []
    listafinalTela = []
    for i in range(len(telas)):
        tela = (telas[i])
        ##print('tela -----', tela)
        ##print(type(tela))
        ##print(tela)
        try:  # Se possivel, ele compila as telas do xml
            #tree = ET.parse(TELAS_FOLDER + tela)
            tree = ET.parse(tela)
            telasname.append(str(tela))
            #print('tree-----', tree)
            root = tree.getroot()
            sequence = ET.tostring(root, encoding='utf8').decode('utf8')
            ##print(sequence)
            j = re.compile(r'(parameter name=\"#102\"*.*value=\")\{(.*)\::\[(.*)](.*\w)')
            for match in j.finditer(sequence):
                match4 = match.group(4)
                match3 = match.group(3)
                match2 = match.group(2)
                listafinalTela.append([match3,match4,match2,tela])
            #listafinalTela.append(listaTela)
        except:
            pass
    df=pd.DataFrame(listafinalTela)
    ##print(df)
    df.to_excel("/tmp/Telas_tag.xlsx")
    #print(df)
    #print(listaTela)
    print('passando pelo tags tela')
    return telasname, listafinalTela

def gera_root(l5x_teste):
    print('passando pelo gera root')
    #settings_dir = os.path.dirname(__file__)
    #PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    #PLC_FOLDER = os.path.join(PROJECT_ROOT, 'PLC/')
    #plcs = os.listdir(PLC_FOLDER)
    plcs = l5x_teste
    lista_root=[]
    lista_plcs = []
    print('passando pela listagem gera root')
    print(plcs)
    print(lista_root)
    print(lista_plcs)
    for plc in plcs:
        #print(plc)
        ##print('plcs----', plcs)
        #print('typeplc abaixo')
        #print(type(plc))
        mydoc = ET.parse(plc)
        print('mydoc -----', mydoc)
        root = mydoc.getroot()
        print('root----', root)
        lista_root.append([str(plc),root])
        lista_plcs.append(str(plc))
        print('lista root preenchida', lista_root)
        print('lista plcs preenchida', lista_plcs)
        ##print(str(plc))
        ##print('plcs----', plcs)
        ##print(lista_plcs)
    print('final do gera root')
    return lista_root, lista_plcs


def intlk(l5x_teste,blocoescrita):
    #print('passando pelo intlk ---- l5x_teste------', l5x_teste)
    listaroot,plcs=gera_root(l5x_teste)
    #print('l5xteste do gera lvu', l5x_teste)
    listafinal = []
    for root in listaroot:
        for sheet in root[1].findall(
                f".//Program/Routines/Routine[@Type='FBD']/FBDContent/Sheet/AddOnInstruction[@Name='{blocoescrita}']/.."):
            for bloco in sheet.findall(f".//AddOnInstruction[@Name='{blocoescrita}']"):
                tagname = bloco.attrib["Operand"].replace(f'_{blocoescrita}', '')
                listafinal.append([tagname, tipotag(tagname, root[1]), "",
                                   f"{(tagdesc(tagname, root[1]))}".replace("\n", " ").replace("None", " ")])
                for wire in sheet.xpath(f"./*[contains(@ToParam ,'Inp_Intlk')][not(contains(@ToParam,'StatusOk'))]"):
                    # print(wire.attrib["ToParam"])
                    for IRef in sheet.findall("./IRef[@ID='" + wire.attrib['FromID'] + "']"):
                        tag = IRef.attrib["Operand"].split(".")[0]
                        listafinal.append([tag, tipotag(tag, root[1]), tagname,
                                           f"{(tagdesc(tagname, root[1]))}".replace("\n", " ").replace("None", " ")])
    df = pd.DataFrame(listafinal)
    df.to_excel('/tmp/tagsplcs.xlsx')
    return listafinal, len(listafinal), plcs



def cria_planilha(lst):
    df = pd.DataFrame(lst)
    df.to_excel(f'{lst}.xlsx')

def cruza_tags(telas,plcs):
    listafinalcruzatags=[]
    for i in telas:
        check = False
        for j in plcs:
            if i[1] == j[2]:
                check == True
                listafinalcruzatags.append([j[2],j[0],i[0],i[2],i[3],j[1],j[3]])
        if check == False:
            for j in plcs:
                if i[1] == j[0]:
                    listafinalcruzatags.append(['',i[1],i[0],i[2],i[3],j[1],j[3]])
    df=pd.DataFrame(listafinalcruzatags, columns=['Bloco','Tag', 'Topico', 'Diretorio', 'Tela', 'Tipo', 'Descricao'])
    drop=["BOOL", "P_Logic", "P_Intlk", "TIMER","REAL","DINT"]
    drop.extend(["CLX_CommValor","P_GateStandAlone","P_PF755_Inp"])
    df=df[~df['Tipo'].isin(drop)]
    df.drop_duplicates(keep='first', inplace=True)
    df.reset_index().drop(["index"], axis=1)
    df.to_excel("/tmp/intlk.xlsx")
    return df

tags_geradas = []
def AddTag2(tag,padrao,PollGroupTags,intlk):
    for i in range(len(padrao)):
        ETc.SubElement(PollGroupTags, "Tag").text = tag["Diretorio"]+"::"+"["+tag["Topico"]+ "]" + tag["Tag"] + "." + padrao[i]
        tags_geradas.append([tag,padrao,tag["Diretorio"]+tag["Topico"]+tag["Tag"] + "." + padrao[i]])
    if intlk:
        ETc.SubElement(PollGroupTags, "Tag").text = tag["Diretorio"] +"::"+"["+tag["Topico"]+ "]"+ tag["Tag"] + "_Intlk.Val_FirstOutTxt"
        tags_geradas.append([tag, padrao, tag["Diretorio"] + tag["Topico"] + tag["Tag"] + "_Intlk.Val_FirstOutTxt"])
    if tag["Tipo"] == "P_E300Ovld" or tag["Tipo"] == "P_E3Ovld":
        ETc.SubElement(PollGroupTags, "Tag").text = tag["Diretorio"] +"::"+"["+tag["Topico"]+ "]"+ tag["Tag"] + "_Ovld.Val_WarningCode"
        tags_geradas.append([tag, padrao, tag["Diretorio"] + tag["Topico"] + tag["Tag"] + "_Ovld.Val_WarningCode"])
        ETc.SubElement(PollGroupTags, "Tag").text = tag["Diretorio"] +"::"+"["+tag["Topico"]+ "]"+ tag["Tag"] + "_Ovld.Val_TripCode"
        tags_geradas.append([tag, padrao, tag["Diretorio"] + tag["Topico"] + tag["Tag"] + "_Ovld.Val_TripCode"])

def AddTag(dados, PollGroupTags):
    texto2=""
    arquivo = open('tipos_faltantes.txt', 'w')
    dados=(dados.T)
    #teste = Configuracao.objects.filter(alarme__alarme_objeto__nome= 'Padrao_Ain')
    #c = Alarme.objects.filter(alarme_objeto__nome= 'Padrao_Ain')



    for tags in range(dados.shape[0]):
        tag = dados.iloc[tags, :]
        #print(f"tag={tag[5]}")
        if (tag[5] == "P_VSD"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_PF755"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_Motor"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_MotorRev"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_E300Ovld"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_E3Ovld"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_LLS"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_Dout"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_ValveSO"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_ValveC"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_ValveMO"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_D4SD"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_PIDE"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_Seq"):
            AddTag2(tag, aux, PollGroupTags, True)
        elif (tag[5] == "P_AinAdv"):
            AddTag2(tag, aux, PollGroupTags, False)
        elif (tag[5] == "P_Ain"):
            AddTag2(tag, aux, PollGroupTags, False)
        elif (tag[5] == "P_DinAdv"):
            AddTag2(tag, aux, PollGroupTags, False)
        elif (tag[5] == "P_Din"):
            AddTag2(tag, aux, PollGroupTags, False)
        else:
            texto1 = tag[5]
            if texto1 in texto2:
                pass
            else:
                texto2 = texto2+(f" {tag[5]}")
            #print("Falta Data Type: " + tag[5])
    arquivo.write(texto2)
    arquivo.close()

tags_mensagem = []
tag_msg = []
def AddMessage2(Messages, Tag_MSG, padrao_alm):
    MaxNum = 0
    for m in Messages:
        if MaxNum < int(m.get("id")):
            MaxNum = int(m.get("id"))
    for i in range(len(padrao_alm)):
        message = ETc.SubElement(Messages, "Message")
        message.set("id", str(MaxNum + 1))
        msgs = ETc.SubElement(message, "Msgs")
        #msg1 = ETc.SubElement(msgs, "Msg")
        #msg1.set("xml:lang", "en-US")
        #msg1.text = Padrao_Msg_Text.get(Tag_MSG["Tipo"]).get(padrao_alm[i])[0].replace("DESCRIÇÃO_DA_TAG",Tag_MSG["Descricao"])
        msg1 = ETc.SubElement(msgs, "Msg")
        msg1.set("xml:lang", "pt-BR")
        msg1.text = Padrao_Msg_Text.get(Tag_MSG["Tipo"]).get(padrao_alm[i])[0].replace("DESCRIÇÃO_DA_TAG",Tag_MSG["Descricao"])
        tags_mensagem.append([Tag_MSG["Diretorio"],Tag_MSG["Topico"],Tag_MSG["Tag"],"." + padrao_alm[i],Tag_MSG["Tipo"],str(MaxNum + 1)])
        MaxNum += 1

def AddMessage(dados, Messages):
    #print(dados)

    for tags_msg_Alm in range(dados.shape[0]):
        tag_msg = dados.iloc[tags_msg_Alm, :]
        if (tag_msg[5] == "P_VSD"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_PF755"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_Motor"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_MotorRev"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_E300Ovld"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_E3Ovld"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_LLS"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_Dout"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_ValveSO"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_ValveC"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_ValveMO"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_D4SD"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_PIDE"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_Seq"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_AinAdv"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_Ain"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_DinAdv"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        elif (tag_msg[5] == "P_Din"):
            AddMessage2(Messages, tag_msg, lista_alarmes)
        else:
            pass
            #print("Falta Data Type: " + tag_msg[5])

def AddGrupo(plcs,telas,num_plcs,num_telas,lista_grupo,Groups):
    #print('chegando no add group ')
    grupo_plcs = 1
    grupo_telas = 101
    for i in range(num_plcs):
        Group = ETc.SubElement(Groups, "Group")
        Group.set("id", str(grupo_plcs))
        Group.set("parentID", "0")
        #print('plcs do add_group ------ ',plcs)
        Group.text = plcs[i].replace(".xml","").replace(".L5X","").replace("(","").replace(")","").replace("-","_").replace(" ","_")
        grupo_plcs += 1
    for i in range(num_plcs):
        for j in range(num_telas):
            Group = ETc.SubElement(Groups, "Group")
            Group.set("id", str(grupo_telas))
            Group.set("parentID", str(i + 1))
            Group.text = telas[j].replace(".xml","").replace(".L5X","").replace("(","").replace(")","").replace("-","_").replace(" ","_")
            lista_grupo.iloc[i, j] = grupo_telas
            grupo_telas += 1
        grupo_telas = (100 * (i + 2)) + 1

def AddParam(Tag_MSG, Params):
    #print(Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[1])
    if Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[1] != "":
        Param1 = ETc.SubElement(Params, "Param")
        Param1.set("key", "Tag1")
        Param1.text = Tag_MSG[0] + Tag_MSG[1] + Tag_MSG[2] + str(Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[1])
        #print("primeiro if")
        if Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[2] != "":
            Param2 = ETc.SubElement(Params, "Param")
            Param2.set("key", "Tag2")
            Param2.text = Tag_MSG[0] + Tag_MSG[1] + Tag_MSG[2] + str(Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[2])
            #print("segundo if")
            if Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[3] != "":
                Param3 = ETc.SubElement(Params, "Param")
                Param3.set("key", "Tag3")
                Param3.text = Tag_MSG[0] + Tag_MSG[1] + Tag_MSG[2] + str(Padrao_Msg_Text.get(Tag_MSG[4]).get(Tag_MSG[3].replace(".", ""))[3])
                #print("terceiro if")

#continuar apartir daqui essa bagunça
def AddConfiguracao(FTAlarmElements,tags_mensagem, lista_grupo, dados):  # area, topico, tag, padrao alm(.IOFault), DataType, ID
    #print((tags_mensagem))

    d = dados.copy()
    for i in range(len(tags_mensagem)):
        FTAlarmElement = ETc.SubElement(FTAlarmElements, "FTAlarmElement")
        FTAlarmElement.set("name", (tags_mensagem[i][2] + tags_mensagem[i][3]).replace(".", "_"))
        FTAlarmElement.set("latched", "false")
        FTAlarmElement.set("ackRequired", "true")
        FTAlarmElement.set("style", "Discrete")

        DiscreteElement = ETc.SubElement(FTAlarmElement, "DiscreteElement")

        DataItem = ETc.SubElement(DiscreteElement, "DataItem").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + tags_mensagem[i][3]
        Style = ETc.SubElement(DiscreteElement, "Style").text = "DiscreteTrue"
        Severity = ETc.SubElement(DiscreteElement, "Severity").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + ".Cfg_" + tags_mensagem[i][3].replace(".Alm_","") + "Severity"
        DelayInterval = ETc.SubElement(DiscreteElement, "DelayInterval").text = "0"
        EnableTag = ETc.SubElement(DiscreteElement, "EnableTag").text = "false"
        UserData = ETc.SubElement(DiscreteElement, "UserData")
        RSVCmd = ETc.SubElement(DiscreteElement, "RSVCmd").text = "AE_DisplayQuick " + tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + " " + tags_mensagem[i][0] + tags_mensagem[i][1]
        AlarmClass = ETc.SubElement(DiscreteElement, "AlarmClass").text = tags_mensagem[i][4]

        d2 = d.loc[d["Tag"] == tags_mensagem[i][2]]
        #d2["Tela"] = d2["Tela"]#.map(lambda y: y.replace("(", "").replace(")", "").replace(" ", "_").replace("-", "").replace(".xml",""))
        #d2["Topico"] = d2["Topico"]#.map(lambda y: y.replace("[", "").replace("]", ""))
        plc = d2["Topico"]
        pasta = d2["Tela"]
        #print(lista_grupo.index.get_indexer(plc))
        #l = int(lista_grupo.index.get_indexer(plc))
        l=-1
        c = int(lista_grupo.columns.get_loc(str(list(pasta)[0])))

        GroupID = ETc.SubElement(DiscreteElement, "GroupID").text = str(lista_grupo.iloc[l, c])

        HandshakeTags = ETc.SubElement(DiscreteElement, "HandshakeTags")
        InAlarmDataItem = ETc.SubElement(HandshakeTags, "InAlarmDataItem")
        DisabledDataItem = ETc.SubElement(HandshakeTags, "DisabledDataItem").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_","") + ".Com_AE.9"
        AckedDataItem = ETc.SubElement(HandshakeTags, "AckedDataItem").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.1"
        SuppressedDataItem = ETc.SubElement(HandshakeTags, "SuppressedDataItem").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.6"
        ShelvedDataItem = ETc.SubElement(HandshakeTags, "ShelvedDataItem").text = tags_mensagem[i][0] + tags_mensagem[i][1] + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_","") + ".Com_AE.3"

        RemoteAckAllDataItem = ETc.SubElement(DiscreteElement, "RemoteAckAllDataItem")
        RemoteAckAllDataItem.set("AutoReset", "false")
        RemoteAckAllDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.1"

        RemoteDisableDataItem = ETc.SubElement(DiscreteElement, "RemoteDisableDataItem")
        RemoteDisableDataItem.set("AutoReset", "true")
        RemoteDisableDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.10"

        RemoteEnableDataItem = ETc.SubElement(DiscreteElement, "RemoteEnableDataItem")
        RemoteEnableDataItem.set("AutoReset", "true")
        RemoteEnableDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.11"

        RemoteSuppressDataItem = ETc.SubElement(DiscreteElement, "RemoteSuppressDataItem")
        RemoteSuppressDataItem.set("AutoReset", "true")
        RemoteSuppressDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.7"

        RemoteUnSuppressDataItem = ETc.SubElement(DiscreteElement, "RemoteUnSuppressDataItem")
        RemoteUnSuppressDataItem.set("AutoReset", "true")
        RemoteUnSuppressDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.8"

        RemoteShelveAllDataItem = ETc.SubElement(DiscreteElement, "RemoteShelveAllDataItem")
        RemoteShelveAllDataItem.set("AutoReset", "true")
        RemoteShelveAllDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.4"

        RemoteUnShelveDataItem = ETc.SubElement(DiscreteElement, "RemoteUnShelveDataItem")
        RemoteUnShelveDataItem.set("AutoReset", "true")
        RemoteUnShelveDataItem.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Com_AE.5"

        RemoteShelveDuration = ETc.SubElement(DiscreteElement, "RemoteShelveDuration")
        RemoteShelveDuration.text = tags_mensagem[i][0] + "::" + "[" + tags_mensagem[i][1] + "]" + tags_mensagem[i][2] + tags_mensagem[i][3].replace("Alm_", "") + ".Cfg_MaxShelfT"

        MessageID = ETc.SubElement(DiscreteElement, "MessageID").text = tags_mensagem[i][5]

        Params = ETc.SubElement(DiscreteElement,"Params")  # /Area1/Data3::[Topico]SM_Cal_Parafuso_Intlk.Val_FirstOutTxt
        AddParam(tags_mensagem[i], Params)
        #Param = ETc.SubElement(Params, "Param")
        #Param.set("key","Tag1").text = "Minha Tag para o texto do alarme"


def gera_lvu(xml_teste, l5x_teste):
    print('chegando no gera lvu')
    #listafinal, rnglst, plcs = intlk("C_IntlkProtect")
    plcs, blocoescrita, listafinal = intlk(l5x_teste, 'C_IntlkProtect')
    print('plcs lvu----', plcs)
    print('bloco escrita lvu ------', blocoescrita)
    #listafinal = listafinal
    rnglst = len(listafinal)
    telas, listatelas = tagsTela(xml_teste)
    #listatelas= listatelas
    #listatelas, telas = tagsTela(self=1)
    df = (cruza_tags(listatelas, listafinal))
    lista_tag = df['Tag'].tolist()
    lista_topico = df['Topico'].tolist()
    lista_diretorio = df['Diretorio'].tolist()
    lista_tela = df['Tela'].tolist()
    lista_tipo = df['Tipo'].tolist()

    ### Encontra no primeiro dataframe as telas e relaciona com as tags do PLC e insere em um DataFrame ###


    for i in range(len(lista_tag)):
        for j in range(rnglst):
            var = listafinal[j][0]
            if (lista_tag[i] == var):
                varTop = listafinal[j][2]
                # #print(var)
                # #print(varTop)
                if (lista_topico[i] == varTop):
                    # #print('encontrou')
                    # #print(listafinal[j][1])
                    df_inserido = {'Tag': [listafinal[j][1]],
                                   'Topico': [lista_topico[i]],
                                   'Diretorio': [lista_diretorio[i]],
                                   'Tela': [lista_tela[i]],
                                   'Tipo': [listafinal[j][4]]}
                    df_inserido = pd.DataFrame(data=df_inserido)
                    df = inserir_linha(i + 1, df, df_inserido)

                    ### Remove do Dataframe completo os valores repetidos e deixa só o primeiro encontrado
    result_df = df.drop_duplicates(subset=['Tag'], keep='first')
    ### Mostra os valores duplicados do DataFrame ###
    ### dff = df[df.duplicated(keep=False)] ###
    #result_df.to_csv("CSV.csv", index=False)

    ### Usado para escrever no arquivo lvu ###
    lista_tag1 = result_df['Tag'].tolist()
    lista_topico1 = result_df['Topico'].tolist()
    lista_diretorio1 = result_df['Diretorio'].tolist()
    lista_tela1 = result_df['Tela'].tolist()
    lista_tipo1 = result_df['Tipo'].tolist()

    ### Lista valores unicos dos tipos ###
    provisorio = set(lista_tipo1)
    lista_tipo2 = list(provisorio)

    projeto = 'sinter4/Dados_1'
    arquivo = open('/tmp/alarmes.lvu', 'w')

    texto = ('<?xml version="1.0" encoding="utf-8"?>' + '\n' +
             '<LogixViewProject LastUpdated="09/06/2021 16:34:44" LVU_Version="Version 6.3.0.18">' + '\n' +
             '  <ControllerFiles CurrentControllerName="' + str(plcs[0]) + '">' + '\n')

    arquivo.write(texto)
    arquivo.close()

    arquivo = open('/tmp/alarmes.lvu', 'a')
    for i in range(len(plcs)):
        # plcSemPlant = (plcs[5]).split('_')[0]
        texto = ('    <ControllerFile ControllerName="' + str(plcs[i]).replace(".L5X","") + '" XmlFileName="">' + '\n' +
                 '      <LogixDescFormat>' + '\n' +
                 '        <NumberOfFields>1</NumberOfFields>' + '\n' +
                 '        <Delimiter>vbCrLf</Delimiter>' + '\n' +
                 '        <TagLabelFields>0</TagLabelFields>' + '\n' +
                 '        <TagDescFields>1</TagDescFields>' + '\n' +
                 '        <TagEngineeringUnitFields>0</TagEngineeringUnitFields>' + '\n' +
                 '        <FieldDescriptors>' + '\n' +
                 '          <Field Name="1" Descriptor="" />' + '\n' +
                 '        </FieldDescriptors>' + '\n' +
                 '      </LogixDescFormat>' + '\n' +
                 '    </ControllerFile>' + '\n')
        arquivo.write(texto)

    texto = ('  </ControllerFiles>' + '\n' + '  <HMI>' + '\n')

    arquivo.write(texto)

    for i in range(len(plcs)):
        texto = ('    <ControllerHMI ControllerName="' + str(plcs[i]).replace(".L5X","") + '">' + '\n' +
                 '      <DataServerAreaName>' + projeto + '</DataServerAreaName>' + '\n' +
                 '      <DataServerShortcutName>' + str(plcs[i]).replace(".L5X","").split('_PlantPAx')[0] + '</DataServerShortcutName>' + '\n' +
                 '      <DataServerName>Dados_1</DataServerName>' + '\n' +
                 '      <HmiServerName>HMI projects</HmiServerName>' + '\n' +
                 '      <HmiServerAreaName>' + projeto.split('/')[0] + '</HmiServerAreaName>' + '\n' +
                 '      <HmiDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects</HmiDir>' + '\n' +
                 '      <HmiGfxFileDir />' + '\n' +
                 '      <HmiParFileDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\PAR</HmiParFileDir>' + '\n' +
                 '      <HmiGfxXmlFileDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\gfx_xml</HmiGfxXmlFileDir>' + '\n' +
                 '      <LogixViewHmiXmlFileName>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\LogixView_HMI projects.xml</LogixViewHmiXmlFileName>' + '\n' +
                 '      <ApplicationName>Sinter4_PlantPAx</ApplicationName>' + '\n' +
                 '      <ProductType>RSViewDistributed</ProductType>' + '\n' +
                 '      <HmiLibraryName>EmptyHmiLibrary</HmiLibraryName>' + '\n' +
                 '    </ControllerHMI>' + '\n')
        arquivo.write(texto)

    texto = ('  </HMI>' + '\n' +
             '  <ProjectObjects>' + '\n' +
             '    <ProjectObject Name="Alarmes_CSN" DisplayName="Alarmes_CSN" Desc="" ParentName="" NodeIndex="0">' + '\n' +
             '      <IsSharing>False</IsSharing>' + '\n' +
             '      <SharedBaseObjectName />' + '\n' +
             '      <CanBeShared>False</CanBeShared>' + '\n' +
             '      <Tags />' + '\n' +
             '    </ProjectObject>' + '\n')

    arquivo.write(texto)
    arquivo.close()

    arquivo = open('/tmp/alarmes.lvu', 'a')
    for i in range(len(telas)):
        tela = telas[i]
        texto = ('    <ProjectObject Name="' + str(tela) + '" DisplayName="' + str(tela).replace("(sinter-3) ","").replace(".xml","").replace(" ","_") + '" Desc="" ParentName="Alarmes_CSN" NodeIndex="' + str(i) + '">' + '\n' +
                 '      <IsSharing>False</IsSharing>' + '\n' +
                 '      <SharedBaseObjectName />' + '\n' +
                 '      <CanBeShared>False</CanBeShared>' + '\n' +
                 '      <Tags />' + '\n' +
                 '    </ProjectObject>' + '\n')
        arquivo.write(texto)
    arquivo.close()

    arquivo = open('/tmp/alarmes.lvu', 'a')

    # Percorre Todas as Telas
    for i in range(len(telas)):
        tela = telas[i]
        # Percorre todos os tipos listado unicos
        for j in range(len(lista_tipo2)):
            tipo = lista_tipo2[j]
            texto = ('    <ProjectObject Name="' + str(tipo) + str(i) + '" DisplayName="' + str(tipo) + str(i) + '" Desc="" ParentName="' + str(tela) + '" NodeIndex="' + str(j) + '">' +
                     '\n' + '      <IsSharing>False</IsSharing>' + '\n' +
                     '      <SharedBaseObjectName />' + '\n' +
                     '      <CanBeShared>False</CanBeShared>' + '\n' +
                     '      <Tags>' + '\n')
            arquivo.write(texto)
            # Percorrendo todo o dataframe
            for x in range(len(lista_tag1)):
                if (tela == lista_tela1[x] and tipo == lista_tipo1[x]):
                    texto = ('        <Tag FullLogixTagAddress="' + lista_topico1[x] + '.' + lista_tag1[x] + '" LogixController= "' + lista_topico1[x] + '" LogixName="' + lista_tag1[x] + '" LogixScope="" />' + '\n')
                    arquivo.write(texto)
            texto = ('      </Tags>' + '\n' + '    </ProjectObject>' + '\n')
            arquivo.write(texto)
    arquivo.close()

    arquivo = open('/tmp/alarmes.lvu', 'a')
    texto = ('  </ProjectObjects>' + '\n' + '  <ProjectObjects_LogixCodes />' + '\n' +
             '<ProjectObjects_HmiFiles>' + '\n' +
             '  <ProjectObject_HmiFiles Name="Alarmes_CSN">' + '\n' +
             '    <GfxFiles />' + '\n' +
             '    <GfxXmlFiles />' + '\n' +
             '  </ProjectObject_HmiFiles>' + '\n')
    arquivo.write(texto)

    for i in range(len(telas)):
        texto = ('  <ProjectObject_HmiFiles Name="' + str(telas[i]) + '">' + '\n' +
                 '    <GfxFiles />' + '\n' +
                 '    <GfxXmlFiles />' + '\n' +
                 '  </ProjectObject_HmiFiles>' + '\n')
        arquivo.write(texto)
        i += 1

    texto = ('  </ProjectObjects_HmiFiles>' + '\n'
                                              '  <AlarmServers>' + '\n')
    arquivo.write(texto)
    arquivo.close()

    arquivo = open('/tmp/alarmes.lvu', 'a')
    texto = ('    <AlarmServer Name="Alarmes_1" Desc="" LastAeXmlFileCreatedUsingAlarmGroups="False">' + '\n'
                                                                                                         '      <Controllers>' + '\n')
    arquivo.write(texto)

    for i in range(len(plcs)):
        texto = ('        <Controller ControllerName="' + str(plcs[i]).replace(".L5X","") + '" />' + '\n')
        arquivo.write(texto)
        i += 1

    texto = ('      </Controllers>' + '\n'
                                      '      <Folders />' + '\n'
                                                            '   </AlarmServer>' + '\n'
                                                                                  '  </AlarmServers>' + '\n'
                                                                                                        '  <HistorianServers />' + '\n'
                                                                                                                                   '</LogixViewProject>')

    arquivo.write(texto)
    arquivo.close()


"""def downloadTelastag(request):
    print('entrando agora  na funcao')
    path ="/tmp/Telas_tag.xlsx"
    response = HttpResponse('')
    with open(path, 'rb') as tmp:
        filename= tmp.name.split('/')[-1]
        response = HttpResponse(tmp, content_type='application/text/xml;charset=UTF-8')
        response['Content-Disposition']="attachment; filename=%s" %filename
        print('saindo da funcao')
    return response"""


def adicionaArquivoXml(request):
    if request.method == 'POST':
        form = UploadFileXml(request.POST, request.FILES)
        if form.is_valid():
            xml = request.FILES.getlist('arquivo_xml')
            tagsTela(xml_teste=xml)
            path = "/tmp/Telas_tag.xlsx"
            response = HttpResponse('')
            with open(path, 'rb') as tmp:
                filename = tmp.name.split('/')[-1]
                response = HttpResponse(tmp, content_type='application/text/xml;charset=UTF-8')
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                print('saindo da funcao')
            return response
        return HttpResponse(status=204)
    else:
        form = UploadFileXml()
    return render(request, 'index.html', {'form': form})


def adicionaArquivoL5X(request):
    if request.method == 'POST':
        form = UploadFileL5X(request.POST, request.FILES)
        if form.is_valid():
            l5x = request.FILES.getlist('arquivo_L5X')
            intlk(l5x_teste=l5x, blocoescrita='C_IntlkProtect')
            path = "/tmp/tagsplcs.xlsx"
            response = HttpResponse('')
            with open(path, 'rb') as tmp:
                filename = tmp.name.split('/')[-1]
                response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
                response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        return HttpResponse(status=204)
    else:
        form = UploadFileL5X()
    return render(request, 'l5x.html', {'form': form})


"""def downloadL5X(request):
    path ="/tmp/tagsplcs.xlsx"
    response = HttpResponse('')
    with open(path, 'rb') as tmp:
        filename= tmp.name.split('/')[-1]
        response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
        response['Content-Disposition']="attachment; filename=%s" %filename
    return response"""


def adicionaArquivoLvu(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            l5x = request.FILES.getlist('arquivo_L5X')
            xml = request.FILES.getlist('arquivo_xml')
            #gera_lvu(xml_teste=xml, l5x_teste=l5x)
            gera_xml(xml_teste=xml, l5x_teste= l5x)

            path = "/tmp/xxxxxxxxxxxx.xml"
            response = HttpResponse('')
            with open(path, 'rb') as tmp:
                filename = tmp.name.split('/')[-1]
                response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
                response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        return HttpResponse(status=204)
    else:
        form = UploadFileForm()
    return render(request, 'lvu.html', {'form': form})



"""def downloadLVU(request):
    path ="/tmp/alarmes.lvu"
    response = HttpResponse('')
    with open(path, 'rb') as tmp:
        filename= tmp.name.split('/')[-1]
        response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
        response['Content-Disposition']="attachment; filename=%s" %filename
    return response"""

def adicionaIntlk(request):
    #print(request.FILES)
    if request.method == 'POST':
        #print(request.FILES)

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            l5x = request.FILES.getlist('arquivo_L5X')
            xml = request.FILES.getlist('arquivo_xml')
            gera_lvu(xml_teste=xml, l5x_teste=l5x)
            path = "/tmp/intlk.xlsx"
            response = HttpResponse('')
            with open(path, 'rb') as tmp:
                filename = tmp.name.split('/')[-1]
                response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
                response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        return HttpResponse(status=204)
    else:
        form = UploadFileForm()
    return render(request, 'intlk.html', {'form': form})


"""def downloadIntlk(request):
    path ="/tmp/intlk.xlsx"
    response = HttpResponse('')
    with open(path, 'rb') as tmp:
        filename= tmp.name.split('/')[-1]
        response = HttpResponse(tmp, content_type='application/text/octet-stream;charset=UTF-8')
        response['Content-Disposition']="attachment; filename=%s" %filename
    return response"""



def gera_xml(xml_teste, l5x_teste):
    #listafinal, rnglst, plcs = intlk(text)
    listafinal, blocoescrita, plcs = intlk(l5x_teste, 'C_IntlkProtect')
    #print('lista final geral xml', listafinal)
    telas, listatelas = tagsTela(xml_teste)
    #listatelas, telas = tagsTela(self=1)
    lista_grupo = pd.DataFrame("",plcs,telas)

    df = (cruza_tags(listatelas, listafinal))
    num_telas = len(telas)
    num_plcs = len(plcs)

    root = ETc.Element("FTAeAlarmStore")
    root.set("xmlns:dt", "urn:schemas-microsoft-com:datatypes")
    root.set("xmlns","urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd")
    root.set("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:schemaLocation","urn://www.factorytalk.net/schema/2003/FTLDDAlarms.xsd FTLDDAlarms.xsd")
    Version = ETc.SubElement(root, "Version").text = "11.0.0"
    Commands = ETc.SubElement(root, "Commands")

    FTAeDetectorCommand = ETc.SubElement(Commands, "FTAeDetectorCommand")
    ETc.SubElement(FTAeDetectorCommand, "Operation").text = "SetLanguages"
    Language = ETc.SubElement(FTAeDetectorCommand, "Language")
    Language.set("xml:lang","pt-BR")

    FTAeDetectorCommand2 = ETc.SubElement(Commands, "FTAeDetectorCommand")
    FTAeDetectorCommand2.set("style","FTAeDefaultDetector")
    FTAeDetectorCommand2.set("version","11.0.0")

    ETc.SubElement(FTAeDetectorCommand2, "Operation").text = "SetDAPollGroups"

    PollGroups = ETc.SubElement(FTAeDetectorCommand2, "PollGroups")
    PollGroupTags1 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags1.set("rate","0.10")
    PollGroupTags1.text=" "

    PollGroupTags2 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags2.set("rate","0.25")
    PollGroupTags2.text=" "

    PollGroupTags3 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags3.set("rate","0.50")
    PollGroupTags3.text=" "

    PollGroupTags4 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags4.set("rate","1")
    PollGroupTags4.text=" "

    PollGroupTags5 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags5.set("rate","2")

    AddTag(df.T,PollGroupTags5)

    PollGroupTags6 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags6.set("rate","5")
    PollGroupTags6.text=" "

    PollGroupTags7 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags7.set("rate","10")
    PollGroupTags7.text=" "

    PollGroupTags8 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags8.set("rate","20")
    PollGroupTags8.text=" "

    PollGroupTags9 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags9.set("rate","30")
    PollGroupTags9.text=" "

    PollGroupTags10 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags10.set("rate","60")
    PollGroupTags10.text=" "

    PollGroupTags11 = ETc.SubElement(PollGroups , "PollGroupTags")
    PollGroupTags11.set("rate","120")
    PollGroupTags11.text=" "

    FTAeDetectorCommand3 = ETc.SubElement(Commands, "FTAeDetectorCommand")
    FTAeDetectorCommand3.set("style","FTAeDefaultDetector")
    FTAeDetectorCommand3.set("version","11.0.0")
    ETc.SubElement(FTAeDetectorCommand3, "Operation").text = "WriteMsg"
    Messages = ETc.SubElement(FTAeDetectorCommand3, "Messages")

    AddMessage(df,Messages)

    FTAeDetectorCommand4 = ETc.SubElement(Commands, "FTAeDetectorCommand")
    FTAeDetectorCommand4.set("style","FTAeDefaultDetector")
    FTAeDetectorCommand4.set("version","11.0.0")

    ETc.SubElement(FTAeDetectorCommand4, "Operation").text = "WriteAlarmGroup"
    Groups = ETc.SubElement(FTAeDetectorCommand4, "Groups")
    #print('plcs do add group ----', plcs)
    AddGrupo(plcs,telas,num_plcs,num_telas,lista_grupo,Groups)

    FTAeDetectorCommand5 = ETc.SubElement(Commands, "FTAeDetectorCommand")
    FTAeDetectorCommand5.set("style","FTAeDefaultDetector")
    FTAeDetectorCommand5.set("version","11.0.0")

    ETc.SubElement(FTAeDetectorCommand5, "Operation").text = "WriteConfig"

    FTAlarmElements = ETc.SubElement(FTAeDetectorCommand5,"FTAlarmElements")
    FTAlarmElements.set("shelveMaxValue","480")

    #df2=pd.DataFrame(tags_mensagem)
    #df2.drop_duplicates(subset=2, keep='first', inplace=True)
    #tags_mensagem=df2.values.tolist()
    AddConfiguracao(FTAlarmElements,tags_mensagem, lista_grupo, df)

    tree = ETc.ElementTree(root)
    root = tree.getroot()
    ETc.indent(tree, space="\t", level=0)
    tree.write("/tmp/xxxxxxxxxxxx.xml", xml_declaration=True, encoding='utf-16')


