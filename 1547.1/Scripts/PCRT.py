"""
The phase-angle change ride-through (PCRT) test verifies the ability of the EUT to ride through sudden voltage
phase-angle changes without tripping in accordance with the requirements in 6.5.2.6 of IEEE Std 1547-2018.

Initial Script: 2-4-20, jjohns2@sandia.gov

"""

import sys
import os
import traceback
from svpelab import hil
from svpelab import das
from svpelab import p1547
import script


def test_run():

    result = script.RESULT_PASS
    phil = None
    daq = None
    dataset_filename = None
    ds = None
    result_params = None

    try:
        open_proj = ts.param_value('hil_config.open')
        compilation = ts.param_value('hil_config.compile')
        stop_sim = ts.param_value('hil_config.stop_sim')
        load = ts.param_value('hil_config.load')
        execute = ts.param_value('hil_config.execute')
        model_name = ts.param_value('hil_config.model_name')

        test_num = ts.param_value('phase_jump.test_num')
        eut_startup_time = ts.param_value('phase_jump.eut_startup_time')

        # initialize the hardware in the loop
        phil = hil.hil_init(ts)

        # initialize the das
        daq = das.das_init(ts)

        if phil is not None:
            ts.log("{}".format(phil.info()))
            if open_proj == 'Yes':
                phil.open()

        '''
                                            Table 9 - PCRT (variation 1)
        |----------------------------------------------------------------------------------------------------------
        | Test           | Phase A Voltage Angle | Phase B Voltage Angle | Phase C Voltage Angle | Duration(s)    |
        | Condition      | (degrees, relative to | (degrees, relative to | (degrees, relative to |                |
        |                | initial phase A angle)| initial phase A angle)| initial phase A angle)|                |
        -----------------------------------------------------------------------------------------------------------
            A                   0                       120                     240                   30-40 
            B                   60 or 300               120                     240                 0.320-0.500
            C                   0                       60 or 180               240                 0.320-0.500
            D                   0                       120                     180 or 300          0.320-0.500
            E                   20                      140                     260                   55-65 
            F                   340                     100                     220                   55-65 
        -----------------------------------------------------------------------------------------------------------
        NOTE 1 - All single - phase angle values are specified in the same direction, leading or lagging relative 
                 to the initial phase angle of an arbitrarily assigned phase A during test condition A.
        NOTE 2 - In some test cases two phase angles are given to allow for either forward (leading) or reverse 
                 (lagging) phase shift, and either test condition may be used.
        -----------------------------------------------------------------------------------------------------------        
        '''
        parameters = []
        phase_jump_time = eut_startup_time + 5
        if test_num == 1:
            stop_time = phase_jump_time + 2
            ts.log('Configuring the Opal Simulation to Run Test 1, Variation 1 (A-B-A).')
            # Phase A Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch1/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch2/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', 0))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', 60))
            # Phase B Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch3/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch4/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B0/Value', 120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B1/Value', 120))
            # Phase C Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch7/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch8/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', -120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -120))
            # Trigger Signal Switching times and Magnitude
            parameters.append((model_name + '/SM_Source/Switch5/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch6/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Trigger Low/Value', 0))
            parameters.append((model_name + '/SM_Source/Trigger High/Value', 5))
            # Time to begin the data capture
            parameters.append((model_name + '/SM_Source/Trigger Time/Value', phase_jump_time - 0.5))
        elif test_num == 2:
            stop_time = phase_jump_time + 2
            ts.log('Configuring the Opal Simulation to Run Test 2, Variation 1 (A-C-A).')
            # Phase A Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch1/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch2/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', 0))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', 0))
            # Phase B Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch3/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch4/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B0/Value', 120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B1/Value', 180))
            # Phase C Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch7/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch8/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', -120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -120))
            # Trigger Signal Switching times and Magnitude
            parameters.append((model_name + '/SM_Source/Switch5/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch6/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Trigger Low/Value', 0))
            parameters.append((model_name + '/SM_Source/Trigger High/Value', 5))
            parameters.append((model_name + '/SM_Source/Trigger Time/Value', phase_jump_time - 0.5))
        elif test_num == 3:
            stop_time = phase_jump_time + 2
            ts.log('Configuring the Opal Simulation to Run Test 3, Variation 1 (A-D-A).')
            # Phase A Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch1/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch2/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', 0))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', 0))
            # Phase B Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch3/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Switch4/Threshold', stop_time))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B0/Value', 120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B1/Value', 120))
            # Phase C Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch7/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch8/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', -120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -60))
            # Trigger Signal Switching times and Magnitude
            parameters.append((model_name + '/SM_Source/Switch5/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch6/Threshold', phase_jump_time + 0.5))
            parameters.append((model_name + '/SM_Source/Trigger Low/Value', 0))
            parameters.append((model_name + '/SM_Source/Trigger High/Value', 5))
            parameters.append((model_name + '/SM_Source/Trigger Time/Value', phase_jump_time - 0.5))
        elif test_num == 4:
            stop_time = phase_jump_time + 61
            ts.log('Configuring the Opal Simulation to Run Test 4, Variation 1 (A-E-A).')
            # Phase A Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch1/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch2/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', 0))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', 20))
            # Phase B Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch3/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch4/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B0/Value', 120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B1/Value', 140))
            # Phase C Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch7/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch8/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', -120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -100))
            # Trigger Signal Switching times and Magnitude
            parameters.append((model_name + '/SM_Source/Switch5/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch6/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Trigger Low/Value', 0))
            parameters.append((model_name + '/SM_Source/Trigger High/Value', 5))
            parameters.append((model_name + '/SM_Source/Trigger Time/Value', phase_jump_time - 0.5))
        else:
            stop_time = phase_jump_time + 61
            ts.log('Configuring the Opal Simulation to Run Test 5, Variation 1 (A-F-A).')
            # Phase A Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch1/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch2/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', 0))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -20))
            # Phase B Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch3/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch4/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B0/Value', 120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase B1/Value', 100))
            # Phase C Switching times and Phase Angles
            parameters.append((model_name + '/SM_Source/Switch7/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch8/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A0/Value', -120))
            parameters.append((model_name + '/SM_Source/Phase Angle Phase A1/Value', -140))
            # Trigger Signal Switching times and Magnitude
            parameters.append((model_name + '/SM_Source/Switch5/Threshold', phase_jump_time))
            parameters.append((model_name + '/SM_Source/Switch6/Threshold', phase_jump_time + 60.))
            parameters.append((model_name + '/SM_Source/Trigger Low/Value', 0))
            parameters.append((model_name + '/SM_Source/Trigger High/Value', 5))
            parameters.append((model_name + '/SM_Source/Trigger Time/Value', phase_jump_time - 0.5))

        if phil is not None:
            for p, v in parameters:
                ts.log_debug('Setting %s = %s' % (p, v))
                phil.set_params(p, v)

            # phil.get_parameters(verbose=True)
            # phil.get_signals(verbose=True)

            ts.log('Stop time set to %s' % phil.set_stop_time(stop_time))

            if compilation == 'Yes':
                ts.log("    Model ID: {}".format(phil.compile_model().get("modelId")))
            if stop_sim == 'Yes':
                ts.log("    {}".format(phil.stop_simulation()))
            if load == 'Yes':
                ts.log("    {}".format(phil.load_model_on_hil()))
            if execute == 'Yes':
                ts.log("    {}".format(phil.start_simulation()))

            sim_time = phil.get_time()
            while (stop_time-sim_time) > 1.0:  # final sleep will get to stop_time.
                sim_time = phil.get_time()
                ts.log('Sim Time: %s.  Waiting another %s sec before saving data.' % (sim_time, stop_time-sim_time))
                ts.sleep(1)

        # complete data capture
        ts.log('Waiting 10 seconds for Opal to save the waveform data.')
        ts.sleep(10)
        ts.log('Processing waveform dataset')
        ds = daq.waveform_capture_dataset()
        dataset_filename = 'PhaseJump_%s.csv' % test_num
        ts.log('------------{}------------'.format(dataset_filename))
        ts.log('Saving file: %s' % dataset_filename)
        ds.to_csv(ts.result_file_path(dataset_filename))

        # lib_1547 = p1547.module_1547(ts=ts, aif='VV', imbalance_angle_fix=imbalance_fix)
        # ts.log_debug('1547.1 Library configured for %s' % lib_1547.get_test_name())
        # result_params = lib_1547.get_rslt_param_plot()  # Get the rslt parameters for plot
        # result_params['plot.title'] = dataset_filename.split('.csv')[0]

        result_params = {
            'plot.title': 'Phase Jump',
            'plot.x.title': 'Time (sec)',
            'plot.x.points': 'TIME',
            'plot.y.points': 'AC_V_1', #'AC_V_2', 'AC_V_3',
            'plot.y.title': 'Voltage (V)',
            'plot.y2.points': 'AC_I_1', #'AC_I_2', 'AC_I_3',
            'plot.y2.title': 'Current (A)',
            # 'plot.%s_TARGET.min_error' % y: '%s_TARGET_MIN' % y,
            # 'plot.%s_TARGET.max_error' % y: '%s_TARGET_MAX' % y,
        }

        ts.result_file(dataset_filename, params=result_params)
        result = script.RESULT_COMPLETE

    except script.ScriptFail as e:
        reason = str(e)
        if reason:
            ts.log_error(reason)
    finally:
        if phil is not None:
            phil.close()
        if daq is not None:
            daq.close()
        # if dataset_filename is not None and ds is not None and result_params is not None:
        #     ts.log('Saving file: %s' % dataset_filename)
        #     ds.to_csv(ts.result_file_path(dataset_filename))
        #     ts.result_file(dataset_filename, params=result_params)

    return result


def run(test_script):

    try:
        global ts
        ts = test_script
        rc = 0
        result = script.RESULT_COMPLETE

        ts.log_debug('')
        ts.log_debug('**************  Starting %s  **************' % (ts.config_name()))
        ts.log_debug('Script: %s %s' % (ts.name, ts.info.version))
        ts.log_active_params()

        ts.svp_version(required='1.5.9')

        result = test_run()

        ts.result(result)
        if result == script.RESULT_FAIL:
            rc = 1

    except Exception as e:
        ts.log_error('Test script exception: %s' % traceback.format_exc())
        rc = 1

    sys.exit(rc)


info = script.ScriptInfo(name=os.path.basename(__file__), run=run, version='1.0.0')
# Data acquisition
info.param_group('hil_config', label='HIL Configuration')
info.param('hil_config.open', label='Open Project?', default="Yes", values=["Yes", "No"])
info.param('hil_config.compile', label='Compilation needed?', default="Yes", values=["Yes", "No"])
info.param('hil_config.stop_sim', label='Stop the simulation before loading/execution?',
           default="Yes", values=["Yes", "No"])
info.param('hil_config.load', label='Load the model to target?', default="Yes", values=["Yes", "No"])
info.param('hil_config.execute', label='Execute the model to target?', default="Yes", values=["Yes", "No"])
info.param('hil_config.model_name', label='Model Name', default="Phase_Jump_A_B_A")

info.param_group('phase_jump', label='IEEE 1547.1 Phase Jump Configuration')
info.param('phase_jump.test_num', label='Test Number (1-5)', default=1)
info.param('phase_jump.eut_startup_time', label='EUT Startup Time (s)', default=85)

hil.params(info)
das.params(info)


def script_info():
    
    return info


if __name__ == "__main__":

    # stand alone invocation
    config_file = None
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    params = None

    test_script = script.Script(info=script_info(), config_file=config_file, params=params)
    test_script.log('log it')

    run(test_script)



