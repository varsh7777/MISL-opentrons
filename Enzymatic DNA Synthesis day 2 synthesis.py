from opentrons import protocol_api
import pandas as pd
import numpy as np

metadata = {
    'apiLevel': '23.13',
    'protocolName': 'Enzymatic DNA Synthesis',
    'description': '''This is for the synthesis portion of day 2
                      of Kingsley's DNA synthesis protocol.
                      This program takes in an input of 4 8x12 matricies.

                      Each matrix corresponds to the amount of each dNTP
                      we want to input into each well in the 96 well plate.
                    fin.''',
    'author': 'Sri Varshitha Pinnaka'
    }

dATP_array = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

dCTP_array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

dTTP_array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

dGTP_array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

dNTP_list = [dATP_array, dCTP_array, dTTP_array, dGTP_array]


def run(protocol: protocol_api.ProtocolContext):
    # probably should load data here
    # for now, just using dummy arrays until i get Kingsley's script

    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
    tiprack2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 7)
    # should change this to be
    pipette1 = protocol.load_instrument('p300_single_gen2', 'right',
                                        tip_racks=[tiprack1])
    pipette2 = protocol.load_instrument('p20_single_gen2', 'left',
                                        tip_racks=[tiprack2])

    trough = protocol.load_labware('nest_12_reservoir_15ml', 3)
    plate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    current_pipette = pipette1

    # depositing dATP
    for dNTP in dNTP_list:
        for i in range(8):
            for j in range(12):
                if (dNTP[i][j] > 20):
                    current_pipette = pipette2
                else:
                    current_pipette = pipette1

                current_pipette.pick_up_tip()
                current_pipette.aspirate(dNTP[i][j], trough['A1'], rate=0.1)
                protocol.delay(seconds=2)
                current_pipette.blow_out(plate['A' + str(j + 1)])
                protocol.delay(seconds=2)
                current_pipette.drop_tip()
