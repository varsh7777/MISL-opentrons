from opentrons import protocol_api

# i figured it would be easier to just copy+paste
# the volumes you need each time, but i can change
# this in the future
source_volumes = {40, 0, 12, 34, 18, 56, 17, 14, 42, 12, 34, 18,
                  41, 23, 23, 30, 23, 23, 23, 23, 22, 16, 23, 23,
                  56, 12, 12, 34, 12, 34, 12, 34, 18, 18, 12, 34,
                  23, 0, 23, 90, 0, 90, 0, 90, 23, 23, 23, 90,
                  12, 0, 0, 34, 23, 23, 42, 13, 12, 34, 32, 13,
                  23, 90, 22, 90, 12, 17, 23, 23, 23, 0, 14, 42,
                  34, 42, 64, 0, 13, 90, 12, 34, 13, 19, 41, 19,
                  90, 21, 42, 17, 21, 42, 23, 0, 15, 42, 19, 13}

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Normalization',
    'description': ''' Given a CSV file with data about how much to
                       transfer from one well plate, this program transfers
                       some amount of fluid from the plate to a new well plate.
                       After that, we supplement the rest with water to
                       complete our dilution. We do this for all the wells
                       to complete our normalization.
                    fin.''',
    'author': 'Sri Varshitha Pinnaka'
    }


def run(protocol: protocol_api.ProtocolContext):
    source_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 3)
    dispense_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 4)
    water_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', 5)
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
    tiprack2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 7)
    pipette1 = protocol.load_instrument('p300_multi_gen2', 'left')
    pipette2 = protocol.load_instrument('p20_multi_gen2', 'right')

    # we need to start picking up tips from the end so that we only pick up
    # one tip at a time with our multi-channel gen2 pipette
    tiprack_reverse = ['H12', 'H11', 'H10', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4',
                       'H3', 'H2', 'H1',
                       'G12', 'G11', 'G10', 'G9', 'G8', 'G7', 'G6', 'G5', 'G4',
                       'G3', 'G2', 'G1',
                       'F12', 'F11', 'F10', 'F9', 'F8', 'F7', 'F6', 'F5', 'F4',
                       'F3', 'F2', 'F1',
                       'E12', 'E11', 'E10', 'E9', 'E8', 'E7', 'E6', 'E5', 'E4',
                       'E3', 'E2', 'E1',
                       'D12', 'D11', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4',
                       'D3', 'D2', 'D1',
                       'C12', 'C11', 'C10', 'C9', 'C8', 'C7', 'C6', 'C5', 'C4',
                       'C3', 'C2', 'C1',
                       'B12', 'B11', 'B10', 'B9', 'B8', 'B7', 'B6', 'B5', 'B4',
                       'B3', 'B2', 'B1',
                       'A12', 'A11', 'A10', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4',
                       'A3', 'A2', 'A1']

    # from the input data, we read each line to figure
    # out how much to transfer to the new well plate
    # essentially, just read every cell in our csv data
    # and transfer exactly that amount to the new well plate.
    # assume that the total volume of our final solution is 150 ul

    i = 0

    for volume in source_volumes:
        if (volume > 20):
            pipette1.pick_up_tip(tiprack1[tiprack_reverse[i]])
            pipette1.aspirate(volume, source_plate[tiprack_reverse[95-i]])
            pipette1.dispense(volume+5, dispense_plate[tiprack_reverse[95-i]])
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip(tiprack2[tiprack_reverse[i]])
            pipette2.aspirate(volume, source_plate[tiprack_reverse[95-i]])
            pipette2.dispense(volume+5, dispense_plate[tiprack_reverse[95-i]])
            pipette2.drop_tip()
        i = i + 1

    # using the same csv data, subtract the value in each
    # cell from 150 to get the amount of water we need to add.

    for volume in source_volumes:
        if ((150 - volume) > 20):
            pipette1.pick_up_tip(tiprack1[tiprack_reverse[i]])
            pipette1.aspirate(150-volume,
                              water_plate[tiprack_reverse[95-i]])
            pipette1.dispense(150-volume+5,
                              dispense_plate[tiprack_reverse[95-i]])
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip(tiprack1[tiprack_reverse[i]])
            pipette2.aspirate(150-volume,
                              water_plate[tiprack_reverse[95-i]])
            pipette2.dispense(150-volume+5,
                              dispense_plate[tiprack_reverse[95-i]])
            pipette2.drop_tip()
