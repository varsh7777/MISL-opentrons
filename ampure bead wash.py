from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Ampure Bead Wash',
    'description': '''Basic ampure bead wash!
                    fin.''',
    'author': 'Sri Varshitha Pinnaka'
    }


def run(protocol: protocol_api.ProtocolContext):
    num_of_columns = 1 #int(input("What is the number of columns? "))
    initial_sample_volume = 50 #int(input("What is the initial sample volume? "))
    final_sample_volume = 30 #int(input("What is the desired final sample volume? "))
    bead_ratio = 2 #int(input("Bead ratio? "))
    etoh_wash_volume = 180 #int(input("EtOH wash volume? "))
    incubation_time = 5 #int(input("Incubation time? "))
    dry_time = 3 #int(input("Dry time? "))

    mag_mod = protocol.load_module('magnetic module gen2', 4)
    mag_plate = mag_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
    tiprack2 = protocol.load_labware('opentrons_96_filtertiprack_20ul', 7)
    pipette1 = protocol.load_instrument('p300_multi_gen2', 'right',
                                        tip_racks=[tiprack1])
    pipette2 = protocol.load_instrument('p20_multi_gen2', 'left',
                                        tip_racks=[tiprack2])

    # the first column contains beads, the third column contains ethanol,
    # the fifth has rsb
    trough = protocol.load_labware('nest_12_reservoir_15ml', 3)

    supern_vol = initial_sample_volume * bead_ratio + initial_sample_volume
    bead_aspirate_vol = initial_sample_volume * bead_ratio

    for i in range(num_of_columns):
        if (bead_aspirate_vol > 20):
            # should i control from where within the tiprack
            # it is picking stuff up? i assume opentrons keeps
            # track of this for us but just in case
            pipette1.pick_up_tip()
            pipette1.aspirate(bead_aspirate_vol, trough['A1'])
            # the computation done for where within the mag plate i want to
            # blow out should work in theory, but should be tested
            pipette1.blow_out(mag_plate['A' + str(i + 1)])
            pipette1.mix(10, supern_vol * 2/3)
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip()
            pipette2.aspirate(bead_aspirate_vol, trough['A1'])
            pipette2.blow_out(mag_plate['A' + str(i + 1)])
            pipette2.mix(10, supern_vol * 2/3)
            pipette2.drop_tip()

    protocol.delay(minutes=incubation_time)
    mag_mod.engage()
    protocol.delay(minutes=incubation_time)

    # remove and discard supernatant
    for i in range(num_of_columns):
        if (supern_vol > 20):
            pipette1.pick_up_tip()
            pipette1.aspirate(supern_vol + 5, mag_plate['A' + str(i + 1)],
                              rate=0.1)
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip()
            pipette2.aspirate(supern_vol + 5, mag_plate['A' + str(i + 1)],
                              rate=0.1)
            pipette2.drop_tip()

    for i in range(2):
        for j in range(num_of_columns):
            if (etoh_wash_volume + 5 > 20):
                pipette1.pick_up_tip()
                pipette1.aspirate(etoh_wash_volume, trough['A3'])
                pipette1.blow_out(mag_plate['A' + str(j + 1)])
                protocol.delay(seconds=30)
                pipette1.aspirate(etoh_wash_volume + 5, rate=0.1)
                pipette1.drop_tip()
            else:
                pipette2.pick_up_tip()
                pipette2.aspirate(etoh_wash_volume, trough['A3'])
                pipette2.blow_out(mag_plate['A' + str(j + 1)])
                protocol.delay(seconds=30)
                pipette2.aspirate(etoh_wash_volume + 5, rate=0.1)
                pipette2.drop_tip()

    # i'm assuming that each column's iteration in the above block
    # takes ten seconds, but i should check this in the lab
    dry_seconds = dry_time * 60 - 10 * (num_of_columns - 1)
    protocol.delay(seconds=dry_seconds)

    mag_mod.disengage()

    # Resuspend beads in (Final_sample_volume + 2.5) uL 10mM Tris
    for i in range(num_of_columns):
        if ((final_sample_volume + 2.5) > 20):
            pipette1.pick_up_tip()
            pipette1.aspirate(final_sample_volume + 2.5, trough['A5'])
            pipette1.blow_out(mag_plate['A' + str(i + 1)])
            pipette1.mix(10, (final_sample_volume + 2.5)/2)
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip()
            pipette2.aspirate(final_sample_volume + 2.5, trough['A5'])
            pipette2.blow_out(mag_plate['A' + str(i + 1)])
            pipette2.mix(10, (final_sample_volume + 2.5)/2)
            pipette2.drop_tip()

    protocol.delay(minutes=incubation_time)
    mag_mod.engage()
    protocol.delay(minutes=incubation_time)

    # Move supernatant to fresh columns
    supern_vol_fin = final_sample_volume + 2.5
    for i in range(num_of_columns):
        if (supern_vol_fin > 20):
            pipette1.pick_up_tip()
            pipette1.aspirate(supern_vol_fin, mag_plate['A' + str(i + 1)],
                              rate=0.1)
            pipette1.blow_out(mag_plate['A' + str(i + num_of_columns + 1)])
            pipette1.drop_tip()
        else:
            pipette2.pick_up_tip()
            pipette2.aspirate(supern_vol_fin, mag_plate['A' + str(i + 1)],
                              rate=0.1)
            pipette2.blow_out(mag_plate['A' + str(i + num_of_columns + 1)])
            pipette2.drop_tip()
