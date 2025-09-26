#!/usr/bin/env python

'''
gg.py: GUI for gpawsolve.py
Usage: $ gg.py
'''
import os, io, sys
from shlex import split
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, BooleanVar, StringVar
import pathlib
import subprocess
import shutil
from ase.visualize import view
from ase.io import read, write
import webbrowser

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
WORK_PATH = os.getcwd()
class gg:
    ''' Main class'''
    Struct = ""
    StructLoaded = False

    def __init__(self, master=None):
        global Geo_optim, Elastic_calcvar, DOS_calcvar, Band_calcvar, Density_calcvar, Optical_calcvar, Spin_calcvar
        global EpsXvar, EpsYvar, EpsZvar, ShearYZvar, ShearXZvar, ShearXYvar, Gammavar, Fix_symmetryvar
        global GW_PPAvar, GW_q0_correctionvar, GW_nblocks_maxvar, Struct, StructLoaded, GW_interpolate_bandvar
        global Ground_calcvar, Phonon_calcvar, Phonon_acoustic_sum_rulevar
        
        url = 'https://sblisesivdin.github.io/gpaw-tools/'
        
        def OpenUrl(url):
            webbrowser.open_new(url)
    
        def onOpen():
            ''' This is the open button's behaviour on the first tab.'''
            global basename, basepath, textfilenamepath
            global Struct, StructLoaded
            textfile = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Open file",
                                                  filetypes = (("CIF files","*.cif"),
                                                  ("All files","*.*")))
            textfilenamepath = textfile
            p = pathlib.PurePath(textfilenamepath)
            basename = StringVar()
            basename = pathlib.Path(textfilenamepath).stem
            basepath = StringVar()
            basepath = p.parents[0]
            #textfile.close()
            self.text1.insert(tk.END, "File opened: "+basename+" \n")

            asestruct = read(textfilenamepath, index='-1')
            Struct = asestruct
            StructLoaded = True
            write(os.path.join(p.parents[0], basename)+'_InitialStructure.png', asestruct)
            self.structureimage = tk.PhotoImage(file=os.path.join(p.parents[0], basename)+'_InitialStructure.png')
            self.button2.configure(image=self.structureimage, style='Toolbutton', text='button2')

            
        def onConfigOpen():
            ''' This is the Configuration file open button's behaviour on the first tab.'''
            global configname
            textfile = filedialog.askopenfilename(initialdir = WORK_PATH, title = "Open file",
                                                  filetypes = (("PY files","*.py"),
                                                  ("All files","*.*")))
            configname = textfile
            # Prepare a temporary config file for process
            shutil.copy2(textfile, os.path.join(WORK_PATH,pathlib.Path(configname).stem+'_temp.py')) 
            configname = os.path.join(WORK_PATH, pathlib.Path(configname).stem+'_temp.py')
            # Loading config file
            sys.path.append(WORK_PATH)
            config = __import__(pathlib.Path(configname).stem)

            
            # There must be some elegant way to do this.
            # Searching in globals() make us to use less parameters in config files. Otherwise not using a variable in
            # a congig file gives errors.
            
            # Mode
            self.text1.insert(tk.END, config.__dict__.keys())
            if 'Mode' in config.__dict__.keys():
                if config.Mode == 'PW':
                    self.Modettk.current(0)
                elif config.Mode == 'PW-GW':
                    self.Modettk.current(1)
                elif config.Mode == 'EXX':
                    self.Modettk.current(2)
                elif config.Mode == 'LCAO':
                    self.Modettk.current(3)
                elif config.Mode == 'FD':
                    self.Modettk.current(4)
                else:
                    self.Modettk.current(0)
            else:
                self.Modettk.current(0)

            # Ground state calculation
            if 'Ground_calc' in config.__dict__.keys():
                if config.Ground_calc == True:
                    Ground_calcvar.set(True)
                else:
                    Ground_calcvar.set(False)
            else:
                Ground_calcvar.set(False)

            # Geometric Optimization   
            if 'Geo_optim' in config.__dict__.keys():
                if config.Geo_optim == True:
                    Geo_optimvar.set(True)
                else:
                    Geo_optimvar.set(False)
            else:
                Geo_optimvar.set(False)
            
            # Elastic calculation    
            if 'Elastic_calc' in config.__dict__.keys():
                if config.Elastic_calc == True:
                    Elastic_calcvar.set(True)
                else:
                    Elastic_calcvar.set(False)
            else:
                Elastic_calcvar.set(False)
                
            # DOS calculation    
            if 'DOS_calc' in config.__dict__.keys():
                if config.DOS_calc == True:
                    DOS_calcvar.set(True)
                else:
                    DOS_calcvar.set(False)
            else:
                DOS_calcvar.set(False)

            # Band calculation
            if 'Band_calc' in config.__dict__.keys():
                if config.Band_calc == True:
                    Band_calcvar.set(True)
                else:
                    Band_calcvar.set(False)
            else:
                Band_calcvar.set(False)

            # Density calculation
            if 'Density_calc' in config.__dict__.keys():
                if config.Density_calc == True:
                    Density_calcvar.set(True)
                else:
                    Density_calcvar.set(False)
            else:
                Density_calcvar.set(False)
                
            # Phonon calculation
            if 'Phonon_calc' in config.__dict__.keys():
                if config.Phonon_calc == True:
                    Phonon_calcvar.set(True)
                else:
                    Phonon_calcvar.set(False)
            else:
                Phonon_calcvar.set(False)

            # Optical calculation
            if 'Optical_calc' in config.__dict__.keys():
                if config.Optical_calc == True:
                    Optical_calcvar.set(True)
                else:
                    Optical_calcvar.set(False)
            else:
                Optical_calcvar.set(False)

            # Optimizer
            if 'Optimizer' in config.__dict__.keys():
                if config.Optimizer == 'QuasiNewton':
                    self.Optimizerttk.current(0)
                elif config.Optimizer == 'GPMin':
                    self.Optimizerttk.current(1)
                elif config.Optimizer == 'LBFGS':
                    self.Optimizerttk.current(2)
                elif config.Optimizer == 'FIRE':
                    self.Optimizerttk.current(3)
                else:
                    self.Optimizerttk.current(0)
            else:
                self.Optimizerttk.current(0)
            
            # Max_F_tolerance
            if 'Max_F_tolerance' in config.__dict__.keys():
                self.Max_F_tolerancettk.delete('0', 'end')
                self.Max_F_tolerancettk.insert('0', config.Max_F_tolerance)
            else:
                self.Max_F_tolerancettk.delete('0', 'end')
                self.Max_F_tolerancettk.insert('0', '0.05')
            
            # Max_step
            if 'Max_step' in config.__dict__.keys():
                self.Max_stepttk.delete('0', 'end')
                self.Max_stepttk.insert('0', config.Max_step)
            else:
                self.Max_stepttk.delete('0', 'end')
                self.Max_stepttk.insert('0', '0.2')
            
            # Alpha
            if 'Alpha' in config.__dict__.keys():
                self.Alphattk.delete('0', 'end')
                self.Alphattk.insert('0', config.Alpha)
            else:
                self.Alphattk.delete('0', 'end')
                self.Alphattk.insert('0', '70.0')

            # Damping
            if 'Damping' in config.__dict__.keys():
                self.Dampingttk.delete('0', 'end')
                self.Dampingttk.insert('0', config.Damping)
            else:
                self.Dampingttk.delete('0', 'end')
                self.Dampingttk.insert('0', '1.0')

            # Hydrostatic pressure
            if 'Hydrostatic_pressure' in config.__dict__.keys():
                self.Hydrostatic_pressurettk.delete('0', 'end')
                self.Hydrostatic_pressurettk.insert('0', config.Hydrostatic_pressure)
            else:
                self.Hydrostatic_pressurettk.delete('0', 'end')
                self.Hydrostatic_pressurettk.insert('0', '0.0')
                        
            # Fix_symmetry    
            if 'Fix_symmetry' in config.__dict__.keys():
                if config.Fix_symmetry == True:
                    Fix_symmetryvar.set(True)
                else:
                    Fix_symmetryvar.set(False)
            else:
                Fix_symmetryvar.set(False)
                
            # Relax cell
            if 'Relax_cell' in config.__dict__.keys():
                if config.Relax_cell[0] == True:
                    EpsXvar.set(True)
                else:
                    EpsXvar.set(False)

                if config.Relax_cell[1] == True:
                    EpsYvar.set(True)
                else:
                    EpsYvar.set(False)

                if config.Relax_cell[2] == True:
                    EpsZvar.set(True)
                else:
                    EpsZvar.set(False)

                if config.Relax_cell[3] == True:
                    ShearYZvar.set(True)
                else:
                    ShearYZvar.set(False)

                if config.Relax_cell[4] == True:
                    ShearXZvar.set(True)
                else:
                    ShearXZvar.set(False)

                if config.Relax_cell[5] == True:
                    ShearXYvar.set(True)
                else:
                    ShearXYvar.set(False)
            else:
                EpsXvar.set(False)
                EpsYvar.set(False)
                EpsZvar.set(False)
                ShearYZvar.set(False)
                ShearXZvar.set(False)
                ShearXYvar.set(False)

            # Cut-off energy
            if 'Cut_off_energy' in config.__dict__.keys():
                self.Cut_off_energyttk.delete('0', 'end')
                self.Cut_off_energyttk.insert('0', config.Cut_off_energy)
            else:
                self.Cut_off_energyttk.delete('0', 'end')
                self.Cut_off_energyttk.insert('0', '340')

            # K-points
            if 'Ground_kpts_x' in config.__dict__.keys():
                self.Ground_kpts_xttk.delete('0', 'end')
                self.Ground_kpts_xttk.insert('0', config.Ground_kpts_x)
                self.Ground_kpts_yttk.delete('0', 'end')
                self.Ground_kpts_yttk.insert('0', config.Ground_kpts_y)
                self.Ground_kpts_zttk.delete('0', 'end')
                self.Ground_kpts_zttk.insert('0', config.Ground_kpts_z)
            else:
                self.Ground_kpts_xttk.delete('0', 'end')
                self.Ground_kpts_xttk.insert('0', '1')
                self.Ground_kpts_yttk.delete('0', 'end')
                self.Ground_kpts_yttk.insert('0', '1')
                self.Ground_kpts_zttk.delete('0', 'end')
                self.Ground_kpts_zttk.insert('0', '1')
                
            # Grid points
            if 'Ground_gpts_x' in config.__dict__.keys():
                self.Ground_gpts_xttk.delete('0', 'end')
                self.Ground_gpts_xttk.insert('0', config.Ground_gpts_x)
                self.Ground_gpts_yttk.delete('0', 'end')
                self.Ground_gpts_yttk.insert('0', config.Ground_gpts_y)
                self.Ground_gpts_zttk.delete('0', 'end')
                self.Ground_gpts_zttk.insert('0', config.Ground_gpts_z)
            else:
                self.Ground_gpts_xttk.delete('0', 'end')
                self.Ground_gpts_xttk.insert('0', '1')
                self.Ground_gpts_yttk.delete('0', 'end')
                self.Ground_gpts_yttk.insert('0', '1')
                self.Ground_gpts_zttk.delete('0', 'end')
                self.Ground_gpts_zttk.insert('0', '1')

            # Gamma
            if 'Gamma' in config.__dict__.keys():
                if config.Gamma == True:
                    Gammavar.set(True)
                else:
                    Gammavar.set(False)
            else:
                Gammavar.set(False)

            # Band path
            if 'Band_path' in config.__dict__.keys():
                self.Band_pathttk.delete('0', 'end')
                self.Band_pathttk.insert('0', config.Band_path)
            else:
                self.Band_pathttk.delete('0', 'end')
                self.Band_pathttk.insert('0', 'GX')

            # N-points
            if 'Band_npoints' in config.__dict__.keys():
                self.Band_npointsttk.delete('0', 'end')
                self.Band_npointsttk.insert('0', config.Band_npoints)
            else:
                self.Band_npointsttk.delete('0', 'end')
                self.Band_npointsttk.insert('0', '61')
                
            # Number of bands
            if 'Band_num_of_bands' in config.__dict__.keys():
                self.Band_num_of_bandsttk.delete('0', 'end')
                self.Band_num_of_bandsttk.insert('0', config.Band_num_of_bands)
            else:
                self.Band_num_of_bandsttk.delete('0', 'end')
                self.Band_num_of_bandsttk.insert('0', '8')
            
            # Setup parameters
            if 'Setup_params' in config.__dict__.keys():
                self.Setup_paramsttk.delete('0', 'end')
                if hasattr(config, 'Setup_params'):
                    self.Setup_paramsttk.insert('0', str(config.Setup_params))
                else:
                    self.Setup_paramsttk.insert('0', '{}')
            else:
                self.Setup_paramsttk.delete('0', 'end')
                self.Setup_paramsttk.insert('0', '{}')

            # XCs
            if 'XC_calc' in config.__dict__.keys():
                if config.XC_calc == 'LDA':
                    self.XC_calcttk.current(0)
                elif config.XC_calc == 'PBE':
                    self.XC_calcttk.current(1)
                elif config.XC_calc == 'GLLBSC':
                    self.XC_calcttk.current(2)
                elif config.XC_calc == 'revPBE':
                    self.XC_calcttk.current(3)
                elif config.XC_calc == 'RPBE':
                    self.XC_calcttk.current(4)
                elif config.XC_calc == 'PBE0':
                    self.XC_calcttk.current(5)
                elif config.XC_calc == 'HSE06':
                    self.XC_calcttk.current(6)
                else:
                    self.XC_calcttk.current(0)
            else:
                self.XC_calcttk.current(0)

            # Ground_convergence
            if 'Ground_convergence' in config.__dict__.keys():
                self.Ground_convergencettk.delete('0', 'end')
                if hasattr(config, 'Ground_convergence'):
                    self.Ground_convergencettk.insert('0', str(config.Ground_convergence))
                else:
                    self.Ground_convergencettk.insert('0', '{}')
            else:
                self.Ground_convergencettk.delete('0', 'end')
                self.Ground_convergencettk.insert('0', '{}')

            # Band_convergence
            if 'Band_convergence' in config.__dict__.keys():
                self.Band_convergencettk.delete('0', 'end')
                if hasattr(config, 'Band_convergence'):
                    self.Band_convergencettk.insert('0', str(config.Band_convergence))
                else:
                    self.Band_convergencettk.insert('0', "{'bands':8}")
            else:
                self.Band_convergencettk.delete('0', 'end')
                self.Band_convergencettk.insert('0', "{'bands':8}")

            # Occupation
            if 'Occupation' in config.__dict__.keys():
                self.Occupationttk.delete('0', 'end')
                if hasattr(config, 'Occupation'):
                    self.Occupationttk.insert('0', str(config.Occupation))
                else:
                    self.Occupationttk.insert('0', "{'name': 'fermi-dirac', 'width': 0.05}")
            else:
                self.Occupationttk.delete('0', 'end')
                self.Occupationttk.insert('0', "{'name': 'fermi-dirac', 'width': 0.05}")

            # DOS number of points
            if 'DOS_npoints' in config.__dict__.keys():
                self.DOS_npointsttk.delete('0', 'end')
                self.DOS_npointsttk.insert('0', config.DOS_npoints)
            else:
                self.DOS_npointsttk.delete('0', 'end')
                self.DOS_npointsttk.insert('0', '501')

            # DOS smearing width
            if 'DOS_width' in config.__dict__.keys():
                self.DOS_widthttk.delete('0', 'end')
                self.DOS_widthttk.insert('0', config.DOS_width)
            else:
                self.DOS_widthttk.delete('0', 'end')
                self.DOS_widthttk.insert('0', '0.1')
                
            # DOS_convergence
            if 'DOS_convergence' in config.__dict__.keys():
                self.DOS_convergencettk.delete('0', 'end')
                if hasattr(config, 'DOS_convergence'):
                    self.DOS_convergencettk.insert('0', str(config.DOS_convergence))
                else:
                    self.DOS_convergencettk.insert('0', "{'bands':8}")
            else:
                self.DOS_convergencettk.delete('0', 'end')
                self.DOS_convergencettk.insert('0', "{'bands':8}")
                
            # Number of bands in Bands calculation
            if 'Band_num_of_bands' in config.__dict__.keys():
                self.Band_num_of_bandsttk.delete('0', 'end')
                self.Band_num_of_bandsttk.insert('0', config.Band_num_of_bands)
            else:
                self.Band_num_of_bandsttk.delete('0', 'end')
                self.Band_num_of_bandsttk.insert('0', '8')

            # Spin Calculation
            if 'Spin_calc' in config.__dict__.keys():
                if config.Spin_calc == True:
                    Spin_calcvar.set(True)
                else:
                    Spin_calcvar.set(False)
            else:
                Spin_calcvar.set(False)

            # Magnetic Moment
            if 'Magmom_per_atom' in config.__dict__.keys():
                self.Magmom_per_atomttk.delete('0', 'end')
                self.Magmom_per_atomttk.insert('0', config.Magmom_per_atom)
            else:
                self.Magmom_per_atomttk.delete('0', 'end')
                self.Magmom_per_atomttk.insert('0', '0.0')

            #Gridref for electron density
            if 'Refine_grid' in config.__dict__.keys():
                self.Refine_gridttk.delete('0', 'end')
                self.Refine_gridttk.insert('0', config.Refine_grid)
            else:
                self.Refine_gridttk.delete('0', 'end')
                self.Refine_gridttk.insert('0', '2')
            
            # Total charge
            if 'Total_charge' in config.__dict__.keys():
                self.Total_chargettk.delete('0', 'end')
                self.Total_chargettk.insert('0', config.Magmom_per_atom)
            else:
                self.Total_chargettk.delete('0', 'end')
                self.Total_chargettk.insert('0', '0.0')
                
            # ---------Phonon Parameters--------
            
            # Phonon cut-off energy
            if 'Phonon_PW_cutoff' in config.__dict__.keys():
                self.Phonon_PW_cutoffttk.delete('0', 'end')
                self.Phonon_PW_cutoffttk.insert('0', config.Phonon_PW_cutoff)
            else:
                self.Phonon_PW_cutoffttk.delete('0', 'end')
                self.Phonon_PW_cutoffttk.insert('0', '400')
                
            # Phonon K-points
            if 'Phonon_kpts_x' in config.__dict__.keys():
                self.Phonon_kpts_xttk.delete('0', 'end')
                self.Phonon_kpts_xttk.insert('0', config.Phonon_kpts_x)
                self.Phonon_kpts_yttk.delete('0', 'end')
                self.Phonon_kpts_yttk.insert('0', config.Phonon_kpts_y)
                self.Phonon_kpts_zttk.delete('0', 'end')
                self.Phonon_kpts_zttk.insert('0', config.Phonon_kpts_z)
            else:
                self.Phonon_kpts_xttk.delete('0', 'end')
                self.Phonon_kpts_xttk.insert('0', '3')
                self.Phonon_kpts_yttk.delete('0', 'end')
                self.Phonon_kpts_yttk.insert('0', '3')
                self.Phonon_kpts_zttk.delete('0', 'end')
                self.Phonon_kpts_zttk.insert('0', '3')
             
            # Phonon supercell
            if 'Phonon_supercell' in config.__dict__.keys():
                self.Phonon_supercellttk.delete('0', 'end')
                if hasattr(config, 'Phonon_supercell'):
                    self.Phonon_supercellttk.insert('0', str(config.Phonon_supercell.tolist()))
                else:
                    self.Phonon_supercellttk.insert('0', '[2,2,2]')
            else:
                self.Phonon_supercellttk.delete('0', 'end')
                self.Phonon_supercellttk.insert('0', '[2,2,2]')
                
            # Phonon displacement
            if 'Phonon_displacement' in config.__dict__.keys():
                self.Phonon_displacementttk.delete('0', 'end')
                self.Phonon_displacementttk.insert('0', config.Phonon_displacement)
            else:
                self.Phonon_displacementttk.delete('0', 'end')
                self.Phonon_displacementttk.insert('0', '400')
            
            # Phonon band dispersion path
            if 'Phonon_path' in config.__dict__.keys():
                self.Phonon_pathttk.delete('0', 'end')
                self.Phonon_pathttk.insert('0', config.Phonon_path)
            else:
                self.Phonon_pathttk.delete('0', 'end')
                self.Phonon_pathttk.insert('0', 'GLG')
            
            # Number of points between high symmetry points
            if 'Phonon_npoints' in config.__dict__.keys():
                self.Phonon_npointsttk.delete('0', 'end')
                self.Phonon_npointsttk.insert('0', config.Phonon_npoints)
            else:
                self.Phonon_npointsttk.delete('0', 'end')
                self.Phonon_npointsttk.insert('0', '61')
            
            # Acoustic sum rule for phonon calculation
            if 'Phonon_acoustic_sum_rule' in config.__dict__.keys():
                if config.Phonon_acoustic_sum_rule == True:
                    Phonon_acoustic_sum_rulevar.set(True)
                else:
                    Phonon_acoustic_sum_rulevar.set(False)
            else:
                Phonon_acoustic_sum_rulevar.set(False)
            
            # ---------GW Parameters---------
            
            # GW calculation type
            if 'GW_calc_type' in config.__dict__.keys():
                if config.GW_calc_type == 'GW0':
                    self.GW_calc_typettk.current(0)
                elif config.GW_calc_type == 'G0W0':
                    self.GW_calc_typettk.current(1)
                else:
                    self.GW_calc_typettk.current(0)
            else:
                self.GW_calc_typettk.current(0)
            
            # GWkpoints
            if 'GW_kpoints_list' in config.__dict__.keys():
                self.GW_kpoints_listttk.delete('0', 'end')
                if hasattr(config, 'GW_kpoints_list'):
                    self.GW_kpoints_listttk.insert('0', str(config.GW_kpoints_list.tolist()))
                else:
                    self.GW_kpoints_listttk.insert('0', '[[0.0, 0.0, 0.0], [1 / 3, 1 / 3, 0], [0.0, 0.0, 0.0]]')
            else:
                self.GW_kpoints_listttk.delete('0', 'end')
                self.GW_kpoints_listttk.insert('0', '[[0.0, 0.0, 0.0], [1 / 3, 1 / 3, 0], [0.0, 0.0, 0.0]]')
            
            # GW truncation
            if 'GW_truncation' in config.__dict__.keys():
                if config.GW_truncation is None:
                    self.GW_truncationttk.current(0)
                elif config.GW_truncation == '2D':
                    self.GW_truncationttk.current(1)
                elif config.GW_truncation == '1D':
                    self.GW_truncationttk.current(2)
                elif config.GW_truncation == '0D':
                    self.GW_truncationttk.current(3)
                elif config.GW_truncation == 'wigner-seitz':
                    self.GW_truncationttk.current(4)
                else:
                    self.GW_truncationttk.current(0)
            else:
                self.GW_truncationttk.current(0)

            # GW Cut off energy
            if 'GW_cut_off_energy' in config.__dict__.keys():
                self.GW_cut_off_energyttk.delete('0', 'end')
                self.GW_cut_off_energyttk.insert('0', config.GW_cut_off_energy)
            else:
                self.GW_cut_off_energyttk.delete('0', 'end')
                self.GW_cut_off_energyttk.insert('0', '50')

            # GW valance band number
            if 'GW_valence_band_no' in config.__dict__.keys():
                self.GW_valence_band_nottk.delete('0', 'end')
                self.GW_valence_band_nottk.insert('0', config.GW_valence_band_no)
            else:
                self.GW_valence_band_nottk.delete('0', 'end')
                self.GW_valence_band_nottk.insert('0', '8')

            # GW conduction band number
            if 'GW_conduction_band_no' in config.__dict__.keys():
                self.GW_conduction_band_nottk.delete('0', 'end')
                self.GW_conduction_band_nottk.insert('0', config.GW_conduction_band_no)
            else:
                self.GW_conduction_band_nottk.delete('0', 'end')
                self.GW_conduction_band_nottk.insert('0', '18')

            # GW PPA
            if 'GW_PPA' in config.__dict__.keys():
                if config.GW_PPA == True:
                    GW_PPAvar.set(True)
                else:
                    GW_PPAvar.set(False)
            else:
                GW_PPAvar.set(False)
                
            # GW q0 correction
            if 'GW_q0_correction' in config.__dict__.keys():
                if config.GW_q0_correction == True:
                    GW_q0_correctionvar.set(True)
                else:
                    GW_q0_correctionvar.set(False)
            else:
                GW_q0_correctionvar.set(False)

            # GW nblocks
            if 'GW_nblocks_max' in config.__dict__.keys():
                if config.GW_nblocks_max == True:
                    GW_nblocks_maxvar.set(True)
                else:
                    GW_nblocks_maxvar.set(False)
            else:
                GW_nblocks_maxvar.set(False)

            # GW band interpolation
            if 'GW_interpolate_band' in config.__dict__.keys():
                if config.GW_interpolate_band == True:
                    GW_interpolate_bandvar.set(True)
                else:
                   GW_interpolate_bandvar.set(False)
            else:
                GW_interpolate_bandvar.set(True)

            # ---------Optical------------

            # Type
            if 'Opt_calc_type' in config.__dict__.keys():
                if config.Opt_calc_type == 'BSE':
                    self.Opt_calc_typettk.current(0)
                elif config.Opt_calc_type == 'RPA':
                    self.Opt_calc_typettk.current(1)
                else:
                    self.Opt_calc_typettk.current(0)
            else:
                self.Opt_calc_typettk.current(0)
            
            # Shifting
            if 'Opt_shift_en' in config.__dict__.keys():
                self.Opt_shift_entttk.delete('0', 'end')
                self.Opt_shift_enttk.insert('0', config.Opt_shift_en)
            else:
                self.Opt_shift_enttk.delete('0', 'end')
                self.Opt_shift_enttk.insert('0', '0.0')
            
            # Valance bands for BSE calculation
            if 'Opt_BSE_valence' in config.__dict__.keys():
                self.Opt_BSE_valencettk.delete('0', 'end')
                if hasattr(config, 'Opt_BSE_valence'):
                    self.Opt_BSE_valencettk.insert('0', str(config.Opt_BSE_valence))
                else:
                    self.Opt_BSE_valencettk.insert('0', 'range(0,4)')
            else:
                self.Opt_BSE_valencettk.delete('0', 'end')
                self.Opt_BSE_valencettk.insert('0', 'range(0,4)')
            
            # Conduction bands for BSE calculation
            if 'Opt_BSE_conduction' in config.__dict__.keys():
                self.Opt_BSE_conductionttk.delete('0', 'end')
                if hasattr(config, 'Opt_BSE_conduction'):
                    self.Opt_BSE_conductionttk.insert('0', str(config.Opt_BSE_conduction))
                else:
                    self.Opt_BSE_conductionttk.insert('0', 'range(4,7)')
            else:
                self.Opt_BSE_conductionttk.delete('0', 'end')
                self.Opt_BSE_conductionttk.insert('0', 'range(4,7)')
            
            # Minimum energy value for BSE calculation
            if 'Opt_BSE_min_en' in config.__dict__.keys():
                self.Opt_BSE_min_enttk.delete('0', 'end')
                self.Opt_BSE_min_enttk.insert('0', config.Opt_BSE_min_en)
            else:
                self.Opt_BSE_min_enttk.delete('0', 'end')
                self.Opt_BSE_min_enttk.insert('0', '0.0')
            
            # Maximum energy value for BSE calculation
            if 'Opt_BSE_max_en' in config.__dict__.keys():
                self.Opt_BSE_max_enttk.delete('0', 'end')
                self.Opt_BSE_max_enttk.insert('0', config.Opt_BSE_max_en)
            else:
                self.Opt_BSE_max_enttk.delete('0', 'end')
                self.Opt_BSE_max_enttk.insert('0', '20.0')
            
            # Number of data for BSE calculation
            if 'Opt_BSE_num_of_data' in config.__dict__.keys():
                self.Opt_BSE_num_of_datattk.delete('0', 'end')
                self.Opt_BSE_num_of_datattk.insert('0', config.Opt_BSE_num_of_data)
            else:
                self.Opt_BSE_num_of_datattk.delete('0', 'end')
                self.Opt_BSE_num_of_datattk.insert('0', '1001')
            
            # Number of bands
            if 'Opt_num_of_bands' in config.__dict__.keys():
                self.Opt_num_of_bandsttk.delete('0', 'end')
                self.Opt_num_of_bandsttk.insert('0', config.Opt_num_of_bands)
            else:
                self.Opt_num_of_bandsttk.delete('0', 'end')
                self.Opt_num_of_bandsttk.insert('0', '8')

            # Fermi-Dirac Smearing
            if 'Opt_FD_smearing' in config.__dict__.keys():
                self.Opt_FD_smearingttk.delete('0', 'end')
                self.Opt_FD_smearingttk.insert('0', config.Opt_FD_smearing)
            else:
                self.Opt_FD_smearingttk.delete('0', 'end')
                self.Opt_FD_smearingttk.insert('0', '0.05')

            # Eta
            if 'Opt_eta' in config.__dict__.keys():
                self.Opt_etattk.delete('0', 'end')
                self.Opt_etattk.insert('0', config.Opt_eta)
            else:
                self.Opt_etattk.delete('0', 'end')
                self.Opt_etattk.insert('0', '0.05')

            # DOmega0
            if 'Opt_domega0' in config.__dict__.keys():
                self.Opt_domega0ttk.delete('0', 'end')
                self.Opt_domega0ttk.insert('0', config.Opt_domega0)
            else:
                self.Opt_domega0ttk.delete('0', 'end')
                self.Opt_domega0ttk.insert('0', '0.05')

            # Optical nblocks
            if 'Opt_nblocks' in config.__dict__.keys():
                self.Opt_nblocksttk.delete('0', 'end')
                self.Opt_nblocksttk.insert('0', config.Opt_nblocks)
            else:
                self.Opt_nblocksttk.delete('0', 'end')
                self.Opt_nblocksttk.insert('0', '4')
            
            # Omega2
            if 'Opt_omega2' in config.__dict__.keys():
                self.Opt_omega2ttk.delete('0', 'end')
                self.Opt_omega2ttk.insert('0', config.Opt_omega2)
            else:
                self.Opt_omega2ttk.delete('0', 'end')
                self.Opt_omega2ttk.insert('0', '5.0')

            # Optical cut off
            if 'Opt_cut_of_energy' in config.__dict__.keys():
                self.Opt_cut_of_energyttk.delete('0', 'end')
                self.Opt_cut_of_energyttk.insert('0', config.Opt_cut_of_energy)
            else:
                self.Opt_cut_of_energyttk.delete('0', 'end')
                self.Opt_cut_of_energyttk.insert('0', '100')

            # ----------General------------
            
            #Core number
            if 'MPI_cores' in config.__dict__.keys():
                self.MPI_coresttk.delete('0', 'end')
                self.MPI_coresttk.insert('0', config.MPI_cores)
            else:
                self.MPI_coresttk.delete('0', 'end')
                self.MPI_coresttk.insert('0', '1')
                
            # Max energy for figures
            if 'Energy_max' in config.__dict__.keys():
                self.Energy_maxttk.delete('0', 'end')
                self.Energy_maxttk.insert('0', config.Energy_max)
            else:
                self.Energy_maxttk.delete('0', 'end')
                self.Energy_maxttk.insert('0', '5')
                
            # Min energy for figures
            if 'Energy_min' in config.__dict__.keys():
                self.Energy_minttk.delete('0', 'end')
                self.Energy_minttk.insert('0', config.Energy_min)
            else:
                self.Energy_minttk.delete('0', 'end')
                self.Energy_minttk.insert('0', '-5')
            
            # Text for textbox
            self.text1.insert(tk.END, "Configuration loaded, please continue with Input parameters tab \n")

        def onCalculate():
            '''Calculate button's behaviour'''
            #Firstly, lets save all options to config file.
            with open(configname, 'w') as f1:
                print("import numpy as np", end="\n", file=f1)

                # ---------Ground------------
                if self.Modettk.get() == 'PW':
                    print("Mode = 'PW'", end="\n", file=f1)
                elif self.Modettk.get() == 'PW-GW':
                    print("Mode = 'PW-GW'", end="\n", file=f1)
                elif self.Modettk.get() == 'EXX':
                    print("Mode = 'EXX'", end="\n", file=f1)
                elif self.Modettk.get() == 'LCAO':
                    print("Mode = 'LCAO'", end="\n", file=f1)
                elif self.Modettk.get() == 'FD':
                    print("Mode = 'FD'", end="\n", file=f1)
                else:
                    print("Mode = 'PW'", end="\n", file=f1)
                # Ground_calc
                print("Ground_calc = "+ str(Ground_calcvar.get()), end="\n", file=f1)
                # Geo_optim
                print("Geo_optim = "+ str(Geo_optimvar.get()), end="\n", file=f1)
                # Elastic_calc
                print("Elastic_calc = "+ str(Elastic_calcvar.get()), end="\n", file=f1)
                # DOS_calc
                print("DOS_calc = "+ str(DOS_calcvar.get()), end="\n", file=f1)
                # Band_calc
                print("Band_calc = "+ str(Band_calcvar.get()), end="\n", file=f1)
                # Density_calc
                print("Density_calc = "+ str(Density_calcvar.get()), end="\n", file=f1)
                # Phonon_calc
                print("Phonon_calc = "+ str(Phonon_calcvar.get()), end="\n", file=f1)
                # Optical_calc
                print("Optical_calc = "+ str(Optical_calcvar.get()), end="\n", file=f1)
                # ---------Geometry------------
                # Optimizer
                if self.Optimizerttk.get() == 'PW':
                    print("Optimizer = 'QuasiNewton'", end="\n", file=f1)
                elif self.Optimizerttk.get() == 'PW-GW':
                    print("Optimizer = 'GPMin'", end="\n", file=f1)
                elif self.Optimizerttk.get() == 'EXX':
                    print("Optimizer = 'LBFGS'", end="\n", file=f1)
                elif self.Optimizerttk.get() == 'LCAO':
                    print("Optimizer = 'FIRE'", end="\n", file=f1)
                else:
                    print("Optimizer = 'QuasiNewton'", end="\n", file=f1)
                # Maximum Force tolerance
                print("Max_F_tolerance = "+ str(self.Max_F_tolerancettk.get()), end="\n", file=f1)
                # Max_step
                print("Max_step = "+ str(self.Max_stepttk.get()), end="\n", file=f1)
                # Alpha
                print("Alpha = "+ str(self.Alphattk.get()), end="\n", file=f1)
                # Damping
                print("Damping = "+ str(self.Dampingttk.get()), end="\n", file=f1)
                # Hydrostatic pressure
                print("Hydrostatic_pressure = "+ str(self.Hydrostatic_pressurettk.get()), end="\n", file=f1)
                #Fix_symmetry
                print("Fix_symmetry = "+ str(Fix_symmetryvar.get()), end="\n", file=f1)
                # Cell relaxation
                print("Relax_cell = ["+str(EpsXvar.get())+", "+str(EpsYvar.get())+", "+str(EpsZvar.get())+", "+str(ShearYZvar.get())+", "+str(ShearXZvar.get())+", "+str(ShearXYvar.get())+"]", end="\n", file=f1)

                # ---------Electronic------------
                # Cut_off_energy
                print("Cut_off_energy = "+ str(self.Cut_off_energyttk.get()), end="\n", file=f1)
                # K-points
                print("Ground_kpts_x = "+ str(self.Ground_kpts_xttk.get()), end="\n", file=f1)
                print("Ground_kpts_y = "+ str(self.Ground_kpts_yttk.get()), end="\n", file=f1)
                print("Ground_kpts_z = "+ str(self.Ground_kpts_zttk.get()), end="\n", file=f1)
                # Grid points
                print("Ground_gpts_x = "+ str(self.Ground_gpts_xttk.get()), end="\n", file=f1)
                print("Ground_gpts_y = "+ str(self.Ground_gpts_yttk.get()), end="\n", file=f1)
                print("Ground_gpts_z = "+ str(self.Ground_gpts_zttk.get()), end="\n", file=f1)
                # Gamma
                print("Gamma = "+ str(Gammavar.get()), end="\n", file=f1)
                # Band_path
                print("Band_path = '"+ str(self.Band_pathttk.get())+"'", end="\n", file=f1)
                # Band_npoints
                print("Band_npoints = "+ str(self.Band_npointsttk.get()), end="\n", file=f1)
                # Setup_params
                print("Setup_params = "+ str(self.Setup_paramsttk.get()), end="\n", file=f1)
                # Exchange-Correlation
                if self.XC_calcttk.get() == 'LDA':
                    print("XC_calc = 'LDA'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'PBE':
                    print("XC_calc = 'PBE'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'GLLBSC':
                    print("XC_calc = 'GLLBSC'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'revPBE':
                    print("XC_calc = 'revPBE'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'RPBE':
                    print("XC_calc = 'RPBE'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'PBE0':
                    print("XC_calc = 'PBE0'", end="\n", file=f1)
                elif self.XC_calcttk.get() == 'HSE06':
                    print("XC_calc = 'HSE06'", end="\n", file=f1)
                else:
                    print("XC_calc = 'LDA'", end="\n", file=f1)
                # Ground_convergence
                print("Ground_convergence = "+ str(self.Ground_convergencettk.get()), end="\n", file=f1)
                # Band_convergence
                print("Band_convergence = "+ str(self.Band_convergencettk.get()), end="\n", file=f1)
                # Occupation
                print("Occupation = "+ str(self.Occupationttk.get()), end="\n", file=f1)
                # DOS_npoints
                print("DOS_npoints = "+ str(self.DOS_npointsttk.get()), end="\n", file=f1)
                # DOS_width
                print("DOS_width = "+ str(self.DOS_widthttk.get()), end="\n", file=f1)
                # DOS_convergence
                print("DOS_convergence = "+ str(self.DOS_convergencettk.get()), end="\n", file=f1)
                # Band_num_of_bands
                print("Band_num_of_bands = "+ str(self.Band_num_of_bandsttk.get()), end="\n", file=f1)
                # Spin_calc
                print("Spin_calc = "+ str(Spin_calcvar.get()), end="\n", file=f1)
                # Magmom_per_atom
                print("Magmom_per_atom = "+ str(self.Magmom_per_atomttk.get()), end="\n", file=f1)
                # Refine grid
                print("Refine_grid = "+ str(self.Refine_gridttk.get()), end="\n", file=f1)
                # Total_charge
                print("Total_charge = "+ str(self.Total_chargettk.get()), end="\n", file=f1)
                # ---------Phonon------------
                # Cut_off_energy
                print("Phonon_PW_cutoff = "+ str(self.Phonon_PW_cutoffttk.get()), end="\n", file=f1)
                # K-points
                print("Phonon_kpts_x = "+ str(self.Phonon_kpts_xttk.get()), end="\n", file=f1)
                print("Phonon_kpts_y = "+ str(self.Phonon_kpts_yttk.get()), end="\n", file=f1)
                print("Phonon_kpts_z = "+ str(self.Phonon_kpts_zttk.get()), end="\n", file=f1)
                # Supercell
                print("Phonon_supercell = np.diag("+ str(self.Phonon_supercellttk.get())+")", end="\n", file=f1)
                # Displacement
                print("Phonon_displacement = "+ str(self.Phonon_displacementttk.get()), end="\n", file=f1)
                # Dispersion path
                print("Phonon_path = "+ str(self.Phonon_pathttk.get()), end="\n", file=f1)
                # Number of points
                print("Phonon_npoints = "+ str(self.Phonon_npointsttk.get()), end="\n", file=f1)
                # Acoustic sum rule
                print("Phonon_acoustic_sum_rule = "+ str(Phonon_acoustic_sum_rulevar.get()), end="\n", file=f1)
                # ---------GW Parameters------------
                # GW calculation type
                if self.GW_calc_typettk.get() == 'GW0':
                    print("GW_calc_type = 'GW0'", end="\n", file=f1)
                elif self.GW_calc_typettk.get() == 'G0W0':
                    print("GW_calc_type = 'G0W0'", end="\n", file=f1)
                else:
                    print("GW_calc_type = 'GW0'", end="\n", file=f1)
                # GW truncation
                if self.GW_truncationttk.get() == '':
                    print("GW_truncation = None", end="\n", file=f1)
                elif self.GW_truncationttk.get() == '2D':
                    print("GW_truncation = '2D'", end="\n", file=f1)
                elif self.GW_truncationttk.get() == '1D':
                    print("GW_truncation = '1D'", end="\n", file=f1)
                elif self.GW_truncationttk.get() == '0D':
                    print("GW_truncation = '0D'", end="\n", file=f1)
                else:
                    print("GW_truncation = 'wigner-seitz'", end="\n", file=f1)               
                # GW K-points
                print("GW_kpoints_list = np.array("+ str(self.GW_kpoints_listttk.get())+")", end="\n", file=f1)
                # GW_cut_off_energy
                print("GW_cut_off_energy = "+ str(self.GW_cut_off_energyttk.get()), end="\n", file=f1)
                # GW_valence_band_no
                print("GW_valence_band_no = "+ str(self.GW_valence_band_nottk.get()), end="\n", file=f1)
                # GW_conduction_band_no
                print("GW_conduction_band_no = "+ str(self.GW_conduction_band_nottk.get()), end="\n", file=f1)
                # GW_PPA
                print("GW_PPA = "+ str(GW_PPAvar.get()), end="\n", file=f1)
                # GW q0 correction
                print("GW_q0_correction = "+ str(GW_q0_correctionvar.get()), end="\n", file=f1)
                # GW nblocks maximum split
                print("GW_nblocks_max = "+ str(GW_nblocks_maxvar.get()), end="\n", file=f1)
                # GW band interpolation
                print("GW_interpolate_band = "+ str(GW_interpolate_bandvar.get()), end="\n", file=f1)

                # ---------Optical------------
                # Opt_calc_type
                if self.Opt_calc_typettk.get() == 'BSE':
                    print("Opt_calc_type = 'BSE'", end="\n", file=f1)
                elif self.Opt_calc_typettk.get() == 'RPA':
                    print("Opt_calc_type = 'RPA'", end="\n", file=f1)
                else:
                    print("Opt_calc_type = 'BSE'", end="\n", file=f1)
                # Opt_shift_en
                print("Opt_shift_en = "+ str(self.Opt_shift_enttk.get()), end="\n", file=f1)
                # Opt_BSE_valence
                print("Opt_BSE_valence = "+ str(self.Opt_BSE_valencettk.get()), end="\n", file=f1)
                # Opt_BSE_conduction
                print("Opt_BSE_conduction = "+ str(self.Opt_BSE_conductionttk.get()), end="\n", file=f1)
                # Opt_BSE_min_en
                print("Opt_BSE_min_en = "+ str(self.Opt_BSE_min_enttk.get()), end="\n", file=f1)
                # Opt_BSE_max_en
                print("Opt_BSE_max_en = "+ str(self.Opt_BSE_max_enttk.get()), end="\n", file=f1)
                # Opt_BSE_num_of_data
                print("Opt_BSE_num_of_data = "+ str(self.Opt_BSE_num_of_datattk.get()), end="\n", file=f1)
                # Opt_num_of_bands
                print("Opt_num_of_bands = "+ str(self.Opt_num_of_bandsttk.get()), end="\n", file=f1)
                # Opt_FD_smearing
                print("Opt_FD_smearing = "+ str(self.Opt_FD_smearingttk.get()), end="\n", file=f1)
                # Opt_eta
                print("Opt_eta = "+ str(self.Opt_etattk.get()), end="\n", file=f1)
                # Opt_domega0
                print("Opt_domega0 = "+ str(self.Opt_domega0ttk.get()), end="\n", file=f1)
                # Opt_nblocks
                print("Opt_nblocks = "+ str(self.Opt_nblocksttk.get()), end="\n", file=f1)
                # Opt_omega2
                print("Opt_omega2 = "+ str(self.Opt_omega2ttk.get()), end="\n", file=f1)
                # Opt_cut_of_energy
                print("Opt_cut_of_energy = "+ str(self.Opt_cut_of_energy.get()), end="\n", file=f1)
                
                # ------------Other------------
                # This feature is not used by gpawsolve.py, this is only usable for gg.py
                print("MPI_cores = "+ str(self.MPI_coresttk.get()), end="\n", file=f1)
                # Energy_max
                print("Energy_max = "+ str(self.Energy_maxttk.get()), end="\n", file=f1)
                # Energy_min
                print("Energy_min = "+ str(self.Energy_minttk.get()), end="\n", file=f1)

            # Running the gpawsolve.py. Firstly, let's define a command, then proceed it.
            gpawcommand = 'mpirun -np '+str(self.MPI_coresttk.get())+' gpawsolve.py -d -i '+str(configname)+' -g '+str(textfilenamepath)
            proc = subprocess.Popen(split(gpawcommand), shell=False, stdout = subprocess.PIPE)
            self.text1.insert(tk.END, "Command executed: "+gpawcommand+" \n")

            # Save stdout as a log
            #sys.path.append(os.path.abspath(configname))
            #config = __import__(pathlib.Path(configname).stem)
            
            #Looking for working directory
            if not os.path.isdir(os.path.join(os.path.dirname(configname), basename)):
                os.makedirs(os.path.join(os.path.dirname(configname), basename), exist_ok=True)
            
            with open(os.path.join(os.path.join(os.path.dirname(configname), basename), basename)+"-STDOUT-Log.txt", 'w') as f2:
                for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
                    self.text4.insert(tk.END, line)
                    print(line, end="\n", file=f2)
                self.text1.insert(tk.END, "Calculation finished... \n")
            self.text1.insert(tk.END, "STDOUT is also saved as log file. \n")

            # Read final cif file and save it as png:
            # /home/sblisesivdin/gpaw-tools-main/Cr2O_mp-1206821_primitive/Cr2O_mp-1206821_primitive-STDOUT-Log.txt
            asestruct = read(os.path.join(os.path.join(os.path.dirname(configname), basename), basename)+"-Final.cif", index='-1')
            write(os.path.join(os.path.join(os.path.dirname(configname), basename), basename)+'_FinalStructure.png', asestruct),
            
            shutil.move(os.path.join(basepath, basename)+'_InitialStructure.png', os.path.join(os.path.join(os.path.dirname(configname), basename), basename+'_InitialStructure.png'))
            os.remove(configname)
            self.text1.insert(tk.END, "Initial and Final Structure PNG files are saved to "+os.path.dirname(configname)+"/"+basename+" folder \n")

        def onASEload():
            '''When the user click on the structure image'''
            global Struct, StructLoaded
            if StructLoaded == True:
                # Open ASE GUI
                view(Struct)
        
        # build gui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)

        # --------- Load Structure tab -----------------
        self.frame2 = ttk.Frame(self.toplevel1)
        self.notebookUpper = ttk.Notebook(self.frame2)
        self.frame1 = ttk.Frame(self.notebookUpper)
        self.loadCIFfilettk = ttk.Button(self.frame1)
        self.loadCIFfilettk.configure(state='normal', text='Load Geometry (CIF) File')
        self.loadCIFfilettk.pack(pady='10', side='top')
        self.loadCIFfilettk.configure(command=onOpen)
        
        self.loadConfigfilettk = ttk.Button(self.frame1)
        self.loadConfigfilettk.configure(state='normal', text='Load Input (PY) File')
        self.loadConfigfilettk.pack(pady='10', side='top')
        self.loadConfigfilettk.configure(command=onConfigOpen)

        self.button2 = ttk.Button(self.frame1)
        self.structureimage = tk.PhotoImage(file=os.path.join(PROJECT_PATH,'gui_files/gpaw-tools.png'))
        self.button2.configure(image=self.structureimage, style='Toolbutton', text='button2')
        self.button2.pack(side='top')
        self.button2.configure(command=onASEload)
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(side='top')


        self.notebookUpper.add(self.frame1, text='Load Structure')
        
        # ----------- Input Parameters tab ----------------
        self.frame4 = ttk.Frame(self.notebookUpper)
        self.frame5 = ttk.Frame(self.frame4)
        
        # Labelframe1: Calculator Settings -------------------------------
        self.labelframe1 = ttk.Labelframe(self.frame5)

        # Label
        self.frame6 = ttk.Frame(self.labelframe1)
        self.label1 = ttk.Label(self.frame6)
        self.label1.configure(text='Calculator')
        self.label1.pack(side='left')

        # Mode
        self.Modettk = ttk.Combobox(self.frame6)
        self.Modettk.configure(values=('PW', 'PW-GW', 'EXX', 'LCAO', 'FD'), state='readonly')
        self.Modettk.pack(side='top')
        self.Modettk.current(0)
        self.frame6.configure(height='200', width='200')
        self.frame6.pack(side='top')
        
        # Ground_calc
        self.Ground_calcttk = ttk.Checkbutton(self.labelframe1)
        Ground_calcvar = BooleanVar()
        self.Ground_calcttk.configure(state='normal', variable = Ground_calcvar, onvalue=True, offvalue=False, takefocus=False, text='Ground State Calculation')
        self.Ground_calcttk.pack(side='top')
        
        # Geo_optim
        self.Geo_optimttk = ttk.Checkbutton(self.labelframe1)
        Geo_optimvar = BooleanVar()
        self.Geo_optimttk.configure(state='normal', variable = Geo_optimvar, onvalue=True, offvalue=False, takefocus=False, text='Geometric Optimization')
        self.Geo_optimttk.pack(side='top')
        
        # Elastic_calc
        self.Elastic_calcttk = ttk.Checkbutton(self.labelframe1)
        Elastic_calcvar = BooleanVar()
        self.Elastic_calcttk.configure(state='normal', variable = Elastic_calcvar, onvalue=True, offvalue=False, takefocus=False, text='Elastic Calculation')
        self.Elastic_calcttk.pack(side='top')
        
        # DOS_calc
        self.DOS_calcttk = ttk.Checkbutton(self.labelframe1)
        DOS_calcvar = BooleanVar()
        self.DOS_calcttk.configure(state='normal', variable = DOS_calcvar, onvalue=True, offvalue=False, takefocus=False, text='DOS Calculation')
        self.DOS_calcttk.pack(side='top')
        
        # Band_calc
        self.Band_calcttk = ttk.Checkbutton(self.labelframe1)
        Band_calcvar = BooleanVar()
        self.Band_calcttk.configure(variable = Band_calcvar, onvalue=True, offvalue=False, text='Band Structure Calculation')
        self.Band_calcttk.pack(side='top')
        
        # Density_calc
        self.Density_calcttk = ttk.Checkbutton(self.labelframe1)
        Density_calcvar = BooleanVar()
        self.Density_calcttk.configure(variable = Density_calcvar, onvalue=True, offvalue=False,text='All-Electron Density Calculation')
        self.Density_calcttk.pack(side='top')
        
        # Phonon_calc
        self.Phonon_calcttk = ttk.Checkbutton(self.labelframe1)
        Phonon_calcvar = BooleanVar()
        self.Phonon_calcttk.configure(variable = Phonon_calcvar, onvalue=True, offvalue=False,text='Phonon Calculation')
        self.Phonon_calcttk.pack(side='top')
        
        # Optical_calc
        self.Optical_calcttk = ttk.Checkbutton(self.labelframe1)
        Optical_calcvar = BooleanVar()
        self.Optical_calcttk.configure(variable = Optical_calcvar, onvalue=True, offvalue=False, text='Optical Properties Calculation')
        self.Optical_calcttk.pack(side='top')
        
        # Empty Line
        self.frameEmpty = ttk.Frame(self.labelframe1)
        self.labelEmpty = ttk.Label(self.frameEmpty)
        self.labelEmpty.configure(text=' ')
        self.labelEmpty.pack(side='left')
        self.frameEmpty.configure(height='200', width='200')
        self.frameEmpty.pack(side='top')
        
        # Label
        self.frame28 = ttk.Frame(self.labelframe1)
        self.label1 = ttk.Label(self.frame28)
        self.label1.configure(text='Optimizer')
        self.label1.pack(side='left')
        
        # Optimizer
        self.Optimizerttk = ttk.Combobox(self.frame28)
        self.Optimizerttk.configure(values=('QuasiNewton', 'GPMin', 'LBFGS', 'FIRE'), state='readonly')
        self.Optimizerttk.pack(side='top')
        self.Optimizerttk.current(0)
        self.frame28.configure(height='200', width='200')
        self.frame28.pack(side='top')
        
        # Maximum Force
        self.frame7 = ttk.Frame(self.labelframe1)
        self.label5 = ttk.Label(self.frame7)
        self.label5.configure(text='Maximum Force')
        self.label5.pack(side='left')
        self.Max_F_tolerancettk = ttk.Entry(self.frame7)
        self.Max_F_tolerancettk.delete('0', 'end')
        self.Max_F_tolerancettk.insert('0', '0.05')
        self.Max_F_tolerancettk.pack(side='top')
        self.frame7.configure(height='200', width='200')
        self.frame7.pack(side='top')
        
        # Maximum Step
        self.frameMax_step = ttk.Frame(self.labelframe1)
        self.labelMax_step = ttk.Label(self.frameMax_step)
        self.labelMax_step.configure(text='Maximum Step')
        self.labelMax_step.pack(side='left')
        self.Max_stepttk = ttk.Entry(self.frameMax_step)
        self.Max_stepttk.delete('0', 'end')
        self.Max_stepttk.insert('0', '0.2')
        self.Max_stepttk.pack(side='top')
        self.frameMax_step.configure(height='200', width='200')
        self.frameMax_step.pack(side='top')
        
        # Alpha
        self.frameAlpha = ttk.Frame(self.labelframe1)
        self.labelAlpha = ttk.Label(self.frameAlpha)
        self.labelAlpha.configure(text='Alpha')
        self.labelAlpha.pack(side='left')
        self.Alphattk = ttk.Entry(self.frameAlpha)
        self.Alphattk.delete('0', 'end')
        self.Alphattk.insert('0', '70.0')
        self.Alphattk.pack(side='top')
        self.frameAlpha.configure(height='200', width='200')
        self.frameAlpha.pack(side='top')
        
        # Damping
        self.frameDamping = ttk.Frame(self.labelframe1)
        self.labelDamping = ttk.Label(self.frameDamping)
        self.labelDamping.configure(text='Damping Coef.')
        self.labelDamping.pack(side='left')
        self.Dampingttk = ttk.Entry(self.frameDamping)
        self.Dampingttk.delete('0', 'end')
        self.Dampingttk.insert('0', '1.0')
        self.Dampingttk.pack(side='top')
        self.frameDamping.configure(height='200', width='200')
        self.frameDamping.pack(side='top')

        # Hydrostatic pressure
        self.frameHydrostatic = ttk.Frame(self.labelframe1)
        self.labelHydrostatic = ttk.Label(self.frameHydrostatic)
        self.labelHydrostatic.configure(text='Hydrostatic pressure (GPa)')
        self.labelHydrostatic.pack(side='left')
        self.Hydrostatic_pressurettk = ttk.Entry(self.frameHydrostatic)
        self.Hydrostatic_pressurettk.delete('0', 'end')
        self.Hydrostatic_pressurettk.insert('0', '0.0')
        self.Hydrostatic_pressurettk.pack(side='top')
        self.frameHydrostatic.configure(height='200', width='200')
        self.frameHydrostatic.pack(side='top')
        
        # Fix symmetry during optimization?
        self.frameFix_symmetry = ttk.Frame(self.labelframe1)
        self.Fix_symmetryttk = ttk.Checkbutton(self.frameFix_symmetry)
        Fix_symmetryvar = BooleanVar()
        self.Fix_symmetryttk.configure(variable = Fix_symmetryvar, onvalue=True, offvalue=False, text='Fix Symmetry')
        self.Fix_symmetryttk.pack(side='top')
        self.frameFix_symmetry.configure(height='200', width='200')
        self.frameFix_symmetry.pack(side='top')
        
        self.labelframe1.configure(height='200', text='Run Modes and Geometry Settings', width='200')
        self.labelframe1.pack(side='left')
        # End Labelframe1 ---------------------------------------------------
        
        # Labelframe2: Electronic Calculation Parameters --------------------
        self.labelframe2 = ttk.Labelframe(self.frame5)
 


        # Cut-off energy
        self.frame8 = ttk.Frame(self.labelframe2)
        self.label6 = ttk.Label(self.frame8)
        self.label6.configure(text='Cut-off energy (eV)')
        self.label6.pack(side='left')
        self.Cut_off_energyttk = ttk.Entry(self.frame8)
        self.Cut_off_energyttk.delete('0', 'end')
        self.Cut_off_energyttk.insert('0', '340')
        self.Cut_off_energyttk.pack(side='top')
        self.frame8.configure(height='200', width='200')
        self.frame8.pack(side='top')

        # K-points
        self.frame9 = ttk.Frame(self.labelframe2)
        self.label7 = ttk.Label(self.frame9)
        self.label7.configure(text='K-points (x,y,z)')
        self.label7.pack(side='left')
        self.Ground_kpts_xttk = ttk.Entry(self.frame9)
        self.Ground_kpts_xttk.configure(width='4')
        self.Ground_kpts_xttk.delete('0', 'end')
        self.Ground_kpts_xttk.insert('0', '5')
        self.Ground_kpts_xttk.pack(side='left')
        self.Ground_kpts_yttk = ttk.Entry(self.frame9)
        self.Ground_kpts_yttk.configure(width='4')
        self.Ground_kpts_yttk.delete('0', 'end')
        self.Ground_kpts_yttk.insert('0', '5')
        self.Ground_kpts_yttk.pack(side='left')
        self.Ground_kpts_zttk = ttk.Entry(self.frame9)
        self.Ground_kpts_zttk.configure(width='4')
        self.Ground_kpts_zttk.delete('0', 'end')
        self.Ground_kpts_zttk.insert('0', '5')
        self.Ground_kpts_zttk.pack(side='top')
        self.frame9.configure(height='200', width='200')
        self.frame9.pack(side='top')
        
        # Grid points
        self.frame29 = ttk.Frame(self.labelframe2)
        self.label12 = ttk.Label(self.frame29)
        self.label12.configure(text='Grid points (LCAO only) (x,y,z)')
        self.label12.pack(side='left')
        self.Ground_gpts_xttk = ttk.Entry(self.frame29)
        self.Ground_gpts_xttk.configure(width='4')
        self.Ground_gpts_xttk.delete('0', 'end')
        self.Ground_gpts_xttk.insert('0', '8')
        self.Ground_gpts_xttk.pack(side='left')
        self.Ground_gpts_yttk = ttk.Entry(self.frame29)
        self.Ground_gpts_yttk.configure(width='4')
        self.Ground_gpts_yttk.delete('0', 'end')
        self.Ground_gpts_yttk.insert('0', '8')
        self.Ground_gpts_yttk.pack(side='left')
        self.Ground_gpts_zttk = ttk.Entry(self.frame29)
        self.Ground_gpts_zttk.configure(width='4')
        self.Ground_gpts_zttk.delete('0', 'end')
        self.Ground_gpts_zttk.insert('0', '8')
        self.Ground_gpts_zttk.pack(side='top')
        self.frame29.configure(height='200', width='200')
        self.frame29.pack(side='top')
        
        # Gamma
        self.frame23 = ttk.Frame(self.labelframe2)
        self.Gammattk = ttk.Checkbutton(self.frame23)
        Gammavar = BooleanVar()
        self.Gammattk.configure(variable = Gammavar, onvalue=True, offvalue=False, text='Gamma Included?')
        self.Gammattk.pack(side='top')
        self.frame23.configure(height='200', width='200')
        self.frame23.pack(side='top')
        
        # Band path
        self.frame10 = ttk.Frame(self.labelframe2)
        self.label8 = ttk.Label(self.frame10)
        self.label8.configure(text='Band Path (G:for Gamma)')
        self.label8.pack(side='left')
        self.Band_pathttk = ttk.Entry(self.frame10)
        self.Band_pathttk.delete('0', 'end')
        self.Band_pathttk.insert('0', 'G')
        self.Band_pathttk.pack(side='top')
        self.frame10.configure(height='200', width='200')
        self.frame10.pack(side='top')

        # Number of points
        self.frame11 = ttk.Frame(self.labelframe2)
        self.label9 = ttk.Label(self.frame11)
        self.label9.configure(text='# of points between symmetry points')
        self.label9.pack(side='left')
        self.Band_npointsttk = ttk.Entry(self.frame11)
        self.Band_npointsttk.delete('0', 'end')
        self.Band_npointsttk.insert('0', '61')
        self.Band_npointsttk.pack(side='top')
        self.frame11.configure(height='200', width='200')
        self.frame11.pack(side='top')

        # Setup_params
        self.frameSetup_params = ttk.Frame(self.labelframe2)
        self.labelSetup_params = ttk.Label(self.frameSetup_params)
        self.labelSetup_params.configure(text='Setup parameters({} for none):')
        self.labelSetup_params.pack(side='left')
        self.Setup_paramsttk = ttk.Entry(self.frameSetup_params)
        self.Setup_paramsttk.delete('0', 'end')
        self.Setup_paramsttk.insert('0', '{}')
        self.Setup_paramsttk.pack(side='top')
        self.frameSetup_params.configure(height='200', width='200')
        self.frameSetup_params.pack(side='top')

        # XC
        self.frame14 = ttk.Frame(self.labelframe2)
        self.label11 = ttk.Label(self.frame14)
        self.label11.configure(text='Exchange Correlation')
        self.label11.pack(side='left')
        self.XC_calcttk = ttk.Combobox(self.frame14)
        self.XC_calcttk.configure(values=('LDA', 'PBE', 'GLLBSC', 'revPBE', 'RPBE' , 'PBE0', 'HSE06'), state='readonly')
        self.XC_calcttk.pack(side='top')
        self.XC_calcttk.current(0)
        self.frame14.configure(height='200', width='200')
        self.frame14.pack(side='top')

        # Ground_convergence
        self.frameGround_convergence = ttk.Frame(self.labelframe2)
        self.labelGround_convergence = ttk.Label(self.frameGround_convergence)
        self.labelGround_convergence.configure(text='Convergence for ground calc ({} for def):')
        self.labelGround_convergence.pack(side='left')
        self.Ground_convergencettk = ttk.Entry(self.frameGround_convergence)
        self.Ground_convergencettk.delete('0', 'end')
        self.Ground_convergencettk.insert('0', '{}')
        self.Ground_convergencettk.pack(side='top')
        self.frameGround_convergence.configure(height='200', width='200')
        self.frameGround_convergence.pack(side='top')
        
        # Band_convergence
        self.frameBand_convergence = ttk.Frame(self.labelframe2)
        self.labelBand_convergence = ttk.Label(self.frameBand_convergence)
        self.labelBand_convergence.configure(text='Convergence for band calc ({} for def):')
        self.labelBand_convergence.pack(side='left')
        self.Band_convergencettk = ttk.Entry(self.frameBand_convergence)
        self.Band_convergencettk.delete('0', 'end')
        self.Band_convergencettk.insert('0', "{'bands':8}")
        self.Band_convergencettk.pack(side='top')
        self.frameBand_convergence.configure(height='200', width='200')
        self.frameBand_convergence.pack(side='top')
        
        # Occupation
        self.frameOccupation = ttk.Frame(self.labelframe2)
        self.labelOccupation = ttk.Label(self.frameOccupation)
        self.labelOccupation.configure(text='Occupation ({} for def):')
        self.labelOccupation.pack(side='left')
        self.Occupationttk = ttk.Entry(self.frameOccupation)
        self.Occupationttk.delete('0', 'end')
        self.Occupationttk.insert('0', "{'name': 'fermi-dirac', 'width': 0.05}")
        self.Occupationttk.pack(side='top')
        self.frameOccupation.configure(height='200', width='200')
        self.frameOccupation.pack(side='top')
        
        # DOS number of points
        self.frameDOS_npoints = ttk.Frame(self.labelframe2)
        self.labelDOS_npoints = ttk.Label(self.frameDOS_npoints)
        self.labelDOS_npoints.configure(text='DOS number of points')
        self.labelDOS_npoints.pack(side='left')
        self.DOS_npointsttk = ttk.Entry(self.frameDOS_npoints)
        self.DOS_npointsttk.delete('0', 'end')
        self.DOS_npointsttk.insert('0', '501')
        self.DOS_npointsttk.pack(side='top')
        self.frameDOS_npoints.configure(height='200', width='200')
        self.frameDOS_npoints.pack(side='top')

        # DOS smearing width
        self.frameDOS_width = ttk.Frame(self.labelframe2)
        self.labelDOS_width = ttk.Label(self.frameDOS_width)
        self.labelDOS_width.configure(text='DOS smearing (0.0 for tetrahedron)')
        self.labelDOS_width.pack(side='left')
        self.DOS_widthttk = ttk.Entry(self.frameDOS_width)
        self.DOS_widthttk.delete('0', 'end')
        self.DOS_widthttk.insert('0', '0.1')
        self.DOS_widthttk.pack(side='top')
        self.frameDOS_width.configure(height='200', width='200')
        self.frameDOS_width.pack(side='top')
        
        # DOS convergence
        self.frameDOS_convergence = ttk.Frame(self.labelframe2)
        self.labelDOS_convergence = ttk.Label(self.frameDOS_convergence)
        self.labelDOS_convergence.configure(text='Convergence for DOS calc ({} for def):')
        self.labelDOS_convergence.pack(side='left')
        self.DOS_convergencettk = ttk.Entry(self.frameDOS_convergence)
        self.DOS_convergencettk.delete('0', 'end')
        self.DOS_convergencettk.insert('0', '{}')
        self.DOS_convergencettk.pack(side='top')
        self.frameDOS_convergence.configure(height='200', width='200')
        self.frameDOS_convergence.pack(side='top')
        
        # Number of bands in Band calculation
        self.frameBand_num_of_bands = ttk.Frame(self.labelframe2)
        self.labelBand_num_of_bands = ttk.Label(self.frameBand_num_of_bands)
        self.labelBand_num_of_bands.configure(text='Number of bands')
        self.labelBand_num_of_bands.pack(side='left')
        self.Band_num_of_bandsttk = ttk.Entry(self.frameBand_num_of_bands)
        self.Band_num_of_bandsttk.delete('0', 'end')
        self.Band_num_of_bandsttk.insert('0', '8')
        self.Band_num_of_bandsttk.pack(side='top')
        self.frameBand_num_of_bands.configure(height='200', width='200')
        self.frameBand_num_of_bands.pack(side='top')

        # Spin polarized?
        self.frame15 = ttk.Frame(self.labelframe2)
        self.Spin_calcttk = ttk.Checkbutton(self.frame15)
        Spin_calcvar = BooleanVar()
        self.Spin_calcttk.configure(variable = Spin_calcvar, onvalue=True, offvalue=False, text='Spin-polarized calculation')
        self.Spin_calcttk.pack(side='top')
        self.frame15.configure(height='200', width='200')
        self.frame15.pack(side='top')

        # Magmom_per_atom
        self.frameMagmom_per_atom = ttk.Frame(self.labelframe2)
        self.labelMagmom_per_atom = ttk.Label(self.frameMagmom_per_atom)
        self.labelMagmom_per_atom.configure(text='Magnetic moment per atom')
        self.labelMagmom_per_atom.pack(side='left')
        self.Magmom_per_atomttk = ttk.Entry(self.frameMagmom_per_atom)
        self.Magmom_per_atomttk.delete('0', 'end')
        self.Magmom_per_atomttk.insert('0', '1.0')
        self.Magmom_per_atomttk.pack(side='top')
        self.frameMagmom_per_atom.configure(height='200', width='200')
        self.frameMagmom_per_atom.pack(side='top')
        
        # Grid size
        self.frame16 = ttk.Frame(self.labelframe2)
        self.label13 = ttk.Label(self.frame16)
        self.label13.configure(text='Grid size for electron density calc')
        self.label13.pack(side='left')
        self.Refine_gridttk = ttk.Entry(self.frame16)
        self.Refine_gridttk.delete('0', 'end')
        self.Refine_gridttk.insert('0', '4')
        self.Refine_gridttk.pack(side='top')
        self.frame16.configure(height='200', width='200')
        self.frame16.pack(side='top')
        self.labelframe2.configure(height='200', text='Electronic Calculation Parameters', width='200')
        self.labelframe2.pack(side='left')
        
        # Total_charge
        self.frameTotal_charge = ttk.Frame(self.labelframe2)
        self.labelTotal_charge = ttk.Label(self.frameTotal_charge)
        self.labelTotal_charge.configure(text='Total charge')
        self.labelTotal_charge.pack(side='left')
        self.Total_chargettk = ttk.Entry(self.frameTotal_charge)
        self.Total_chargettk.delete('0', 'end')
        self.Total_chargettk.insert('0', '0.0')
        self.Total_chargettk.pack(side='top')
        self.frameTotal_charge.configure(height='200', width='200')
        self.frameTotal_charge.pack(side='top')
        # End labelframe2 ------------------------------------------
                
        # labelframe3: Optical Calculation Parameters --------------
        self.labelframe3 = ttk.Labelframe(self.frame5)

        # Opt_calc_type
        self.frameOpt_calc_type = ttk.Frame(self.labelframe3)
        self.labelOpt_calc_type = ttk.Label(self.frameOpt_calc_type)
        self.labelOpt_calc_type.configure(text='Optical Calculation Method')
        self.labelOpt_calc_type.pack(side='left')
        self.Opt_calc_typettk = ttk.Combobox(self.frameOpt_calc_type)
        self.Opt_calc_typettk.configure(values=('BSE', 'RPA'), state='readonly')
        self.Opt_calc_typettk.pack(side='top')
        self.Opt_calc_typettk.current(0)
        self.frameOpt_calc_type.configure(height='200', width='200')
        self.frameOpt_calc_type.pack(side='top')
        
        # Opt_shift_en
        self.frameOpt_shift_en = ttk.Frame(self.labelframe3)
        self.labelOpt_shift_en = ttk.Label(self.frameOpt_shift_en)
        self.labelOpt_shift_en.configure(text='Energy shifting in eV')
        self.labelOpt_shift_en.pack(side='left')
        self.Opt_shift_enttk = ttk.Entry(self.frameOpt_shift_en)
        self.Opt_shift_enttk.delete('0', 'end')
        self.Opt_shift_enttk.insert('0', '0.0')
        self.Opt_shift_enttk.pack(side='top')
        self.frameOpt_shift_en.configure(height='200', width='200')
        self.frameOpt_shift_en.pack(side='top')
        
        # Opt_BSE_valence
        self.frameOpt_BSE_valence = ttk.Frame(self.labelframe3)
        self.labelOpt_BSE_valence = ttk.Label(self.frameOpt_BSE_valence)
        self.labelOpt_BSE_valence.configure(text='Valence bands(use range()):')
        self.labelOpt_BSE_valence.pack(side='left')
        self.Opt_BSE_valencettk = ttk.Entry(self.frameOpt_BSE_valence)
        self.Opt_BSE_valencettk.delete('0', 'end')
        self.Opt_BSE_valencettk.insert('0', 'range(0,4)')
        self.Opt_BSE_valencettk.pack(side='top')
        self.frameOpt_BSE_valence.configure(height='200', width='200')
        self.frameOpt_BSE_valence.pack(side='top')
        
        # Opt_BSE_conduction
        self.frameOpt_BSE_conduction = ttk.Frame(self.labelframe3)
        self.labelOpt_BSE_conduction = ttk.Label(self.frameOpt_BSE_conduction)
        self.labelOpt_BSE_conduction.configure(text='Conduction bands(use range()):')
        self.labelOpt_BSE_conduction.pack(side='left')
        self.Opt_BSE_conductionttk = ttk.Entry(self.frameOpt_BSE_conduction)
        self.Opt_BSE_conductionttk.delete('0', 'end')
        self.Opt_BSE_conductionttk.insert('0', 'range(4,7)')
        self.Opt_BSE_conductionttk.pack(side='top')
        self.frameOpt_BSE_conduction.configure(height='200', width='200')
        self.frameOpt_BSE_conduction.pack(side='top')
        
        # Opt_BSE_min_en
        self.frameOpt_BSE_min_en = ttk.Frame(self.labelframe3)
        self.labelOpt_BSE_min_en = ttk.Label(self.frameOpt_BSE_min_en)
        self.labelOpt_BSE_min_en.configure(text='Min. En. for BSE calc.')
        self.labelOpt_BSE_min_en.pack(side='left')
        self.Opt_BSE_min_enttk = ttk.Entry(self.frameOpt_BSE_min_en)
        self.Opt_BSE_min_enttk.delete('0', 'end')
        self.Opt_BSE_min_enttk.insert('0', '0.0')
        self.Opt_BSE_min_enttk.pack(side='top')
        self.frameOpt_BSE_min_en.configure(height='200', width='200')
        self.frameOpt_BSE_min_en.pack(side='top')
        
        # Opt_BSE_max_en
        self.frameOpt_BSE_max_en = ttk.Frame(self.labelframe3)
        self.labelOpt_BSE_max_en = ttk.Label(self.frameOpt_BSE_max_en)
        self.labelOpt_BSE_max_en.configure(text='Max. En. for BSE calc.')
        self.labelOpt_BSE_max_en.pack(side='left')
        self.Opt_BSE_max_enttk = ttk.Entry(self.frameOpt_BSE_max_en)
        self.Opt_BSE_max_enttk.delete('0', 'end')
        self.Opt_BSE_max_enttk.insert('0', '20.0')
        self.Opt_BSE_max_enttk.pack(side='top')
        self.frameOpt_BSE_max_en.configure(height='200', width='200')
        self.frameOpt_BSE_max_en.pack(side='top')
        
        # Opt_BSE_num_of_data
        self.frameOpt_BSE_num_of_data = ttk.Frame(self.labelframe3)
        self.labelOpt_BSE_num_of_data = ttk.Label(self.frameOpt_BSE_num_of_data)
        self.labelOpt_BSE_num_of_data.configure(text='Number of data points')
        self.labelOpt_BSE_num_of_data.pack(side='left')
        self.Opt_BSE_num_of_datattk = ttk.Entry(self.frameOpt_BSE_num_of_data)
        self.Opt_BSE_num_of_datattk.delete('0', 'end')
        self.Opt_BSE_num_of_datattk.insert('0', '1001')
        self.Opt_BSE_num_of_datattk.pack(side='top')
        self.frameOpt_BSE_num_of_data.configure(height='200', width='200')
        self.frameOpt_BSE_num_of_data.pack(side='top')
        
        # Opt_num_of_bands
        self.frame17 = ttk.Frame(self.labelframe3)
        self.label14 = ttk.Label(self.frame17)
        self.label14.configure(text='Number of bands')
        self.label14.pack(side='left')
        self.Opt_num_of_bandsttk = ttk.Entry(self.frame17)
        self.Opt_num_of_bandsttk.delete('0', 'end')
        self.Opt_num_of_bandsttk.insert('0', '16')
        self.Opt_num_of_bandsttk.pack(side='top')
        self.frame17.configure(height='200', width='200')
        self.frame17.pack(side='top')

        # Opt_FD_smearing
        self.frame18 = ttk.Frame(self.labelframe3)
        self.label15 = ttk.Label(self.frame18)
        self.label15.configure(text='Fermi-Dirac smearing value')
        self.label15.pack(side='left')
        self.Opt_FD_smearingttk = ttk.Entry(self.frame18)
        self.Opt_FD_smearingttk.delete('0', 'end')
        self.Opt_FD_smearingttk.insert('0', '0.05')
        self.Opt_FD_smearingttk.pack(side='top')
        self.frame18.configure(height='200', width='200')
        self.frame18.pack(side='top')

        # Opt_eta
        self.frame19 = ttk.Frame(self.labelframe3)
        self.label16 = ttk.Label(self.frame19)
        self.label16.configure(text='Eta value')
        self.label16.pack(side='left')
        self.Opt_etattk = ttk.Entry(self.frame19)
        self.Opt_etattk.delete('0', 'end')
        self.Opt_etattk.insert('0', '0.05')
        self.Opt_etattk.pack(side='top')
        self.frame19.configure(height='200', width='200')
        self.frame19.pack(side='top')

        # Opt_domega0
        self.frame20 = ttk.Frame(self.labelframe3)
        self.label17 = ttk.Label(self.frame20)
        self.label17.configure(text='Domega0 value')
        self.label17.pack(side='left')
        self.Opt_domega0ttk = ttk.Entry(self.frame20)
        self.Opt_domega0ttk.delete('0', 'end')
        self.Opt_domega0ttk.insert('0', '0.02')
        self.Opt_domega0ttk.pack(side='top')
        self.frame20.configure(height='200', width='200')
        self.frame20.pack(side='top')

        # Opt_nblocks
        self.frame21 = ttk.Frame(self.labelframe3)
        self.label18 = ttk.Label(self.frame21)
        self.label18.configure(text='Split matrices in # of blocks')
        self.label18.pack(side='left')
        self.Opt_nblocksttk = ttk.Entry(self.frame21)
        self.Opt_nblocksttk.delete('0', 'end')
        self.Opt_nblocksttk.insert('0', '4')
        self.Opt_nblocksttk.pack(side='top')
        self.frame21.configure(height='200', width='200')
        self.frame21.pack(side='top')

        # Opt_omega2
        self.frameOpt_omega2 = ttk.Frame(self.labelframe3)
        self.labelOpt_omega2 = ttk.Label(self.frameOpt_omega2)
        self.labelOpt_omega2.configure(text='omega2')
        self.labelOpt_omega2.pack(side='left')
        self.Opt_omega2ttk = ttk.Entry(self.frameOpt_omega2)
        self.Opt_omega2ttk.delete('0', 'end')
        self.Opt_omega2ttk.insert('0', '0.05')
        self.Opt_omega2ttk.pack(side='top')
        self.frameOpt_omega2.configure(height='200', width='200')
        self.frameOpt_omega2.pack(side='top')
        
        # Opt_cut_of_energy
        self.frameOpt_cut_of_energy = ttk.Frame(self.labelframe3)
        self.labelOpt_cut_of_energy = ttk.Label(self.frameOpt_cut_of_energy)
        self.labelOpt_cut_of_energy.configure(text='Cut-off en. for opt.')
        self.labelOpt_cut_of_energy.pack(side='left')
        self.Opt_cut_of_energyttk = ttk.Entry(self.frameOpt_cut_of_energy)
        self.Opt_cut_of_energyttk.delete('0', 'end')
        self.Opt_cut_of_energyttk.insert('0', '100')
        self.Opt_cut_of_energyttk.pack(side='top')
        self.frameOpt_cut_of_energy.configure(height='200', width='200')
        self.frameOpt_cut_of_energy.pack(side='top')
        
        self.labelframe3.configure(height='200', text='Optical Calculation Parameters', width='200')
        self.labelframe3.pack(side='left')
        self.frame5.configure(height='200', width='200')
        self.frame5.pack(side='top')
        # End labelframe3 ------------------------------------------

        # Phononframe: Phonon Calculation Parameters --------------
        self.Phononframe = ttk.Labelframe(self.frame5)

        # Phonon_PW_cutoff
        self.framePhonon_PW_cutoff = ttk.Frame(self.Phononframe)
        self.labelPhonon_PW_cutoff = ttk.Label(self.framePhonon_PW_cutoff)
        self.labelPhonon_PW_cutoff.configure(text='Cut-off en.for phonon')
        self.labelPhonon_PW_cutoff.pack(side='left')
        self.Phonon_PW_cutoffttk = ttk.Entry(self.framePhonon_PW_cutoff)
        self.Phonon_PW_cutoffttk.delete('0', 'end')
        self.Phonon_PW_cutoffttk.insert('0', '100')
        self.Phonon_PW_cutoffttk.pack(side='top')
        self.framePhonon_PW_cutoff.configure(height='200', width='200')
        self.framePhonon_PW_cutoff.pack(side='top')
        
        # Phonon K-points
        self.framePhononkpoints = ttk.Frame(self.Phononframe)
        self.labelPhononkpoints = ttk.Label(self.framePhononkpoints)
        self.labelPhononkpoints.configure(text='K-points (x,y,z)')
        self.labelPhononkpoints.pack(side='left')
        self.Phonon_kpts_xttk = ttk.Entry(self.framePhononkpoints)
        self.Phonon_kpts_xttk.configure(width='4')
        self.Phonon_kpts_xttk.delete('0', 'end')
        self.Phonon_kpts_xttk.insert('0', '3')
        self.Phonon_kpts_xttk.pack(side='left')
        self.Phonon_kpts_yttk = ttk.Entry(self.framePhononkpoints)
        self.Phonon_kpts_yttk.configure(width='4')
        self.Phonon_kpts_yttk.delete('0', 'end')
        self.Phonon_kpts_yttk.insert('0', '3')
        self.Phonon_kpts_yttk.pack(side='left')
        self.Phonon_kpts_zttk = ttk.Entry(self.framePhononkpoints)
        self.Phonon_kpts_zttk.configure(width='4')
        self.Phonon_kpts_zttk.delete('0', 'end')
        self.Phonon_kpts_zttk.insert('0', '3')
        self.Phonon_kpts_zttk.pack(side='top')
        self.framePhononkpoints.configure(height='200', width='200')
        self.framePhononkpoints.pack(side='top')
        
        # Phonon_supercell
        self.framePhonon_supercell = ttk.Frame(self.Phononframe)
        self.labelPhonon_supercell = ttk.Label(self.framePhonon_supercell)
        self.labelPhonon_supercell.configure(text='Supercell [x,y,z]')
        self.labelPhonon_supercell.pack(side='left')
        self.Phonon_supercellttk = tk.Entry(self.framePhonon_supercell)
        self.Phonon_supercellttk.delete('0', 'end')
        self.Phonon_supercellttk.insert('0', '[3,3,3]')
        self.Phonon_supercellttk.pack(side='top')
        self.framePhonon_supercell.configure(height='200', width='200')
        self.framePhonon_supercell.pack(side='top')
        
        # Phonon_displacement
        self.framePhonon_displacement = ttk.Frame(self.Phononframe)
        self.labelPhonon_displacement= ttk.Label(self.framePhonon_displacement)
        self.labelPhonon_displacement.configure(text='Displacement')
        self.labelPhonon_displacement.pack(side='left')
        self.Phonon_displacementttk = ttk.Entry(self.framePhonon_displacement)
        self.Phonon_displacementttk.delete('0', 'end')
        self.Phonon_displacementttk.insert('0', '1e-3')
        self.Phonon_displacementttk.pack(side='top')
        self.framePhonon_displacement.configure(height='200', width='200')
        self.framePhonon_displacement.pack(side='top')
        
        # Phonon_path
        self.framePhonon_path = ttk.Frame(self.Phononframe)
        self.labelPhonon_path = ttk.Label(self.framePhonon_path)
        self.labelPhonon_path.configure(text='Dispersion path')
        self.labelPhonon_path.pack(side='left')
        self.Phonon_pathttk = ttk.Entry(self.framePhonon_path)
        self.Phonon_pathttk.delete('0', 'end')
        self.Phonon_pathttk.insert('0', 'LGL')
        self.Phonon_pathttk.pack(side='top')
        self.framePhonon_path.configure(height='200', width='200')
        self.framePhonon_path.pack(side='top')
        
        # Phonon_npoints
        self.framePhonon_npoints = ttk.Frame(self.Phononframe)
        self.labelPhonon_npoints = ttk.Label(self.framePhonon_npoints)
        self.labelPhonon_npoints.configure(text='Number of points')
        self.labelPhonon_npoints.pack(side='left')
        self.Phonon_npointsttk = ttk.Entry(self.framePhonon_npoints)
        self.Phonon_npointsttk.delete('0', 'end')
        self.Phonon_npointsttk.insert('0', '61')
        self.Phonon_npointsttk.pack(side='top')
        self.framePhonon_npoints.configure(height='200', width='200')
        self.framePhonon_npoints.pack(side='top')
        
        # Acoustic_sum_rule
        self.frameAcoustic_sum_rule = ttk.Frame(self.Phononframe)
        self.Acoustic_sum_rulettk = ttk.Checkbutton(self.frameAcoustic_sum_rule)
        Acoustic_sum_rulevar = BooleanVar()
        self.Acoustic_sum_rulettk.configure(variable = Acoustic_sum_rulevar, onvalue=True, offvalue=False, text='Acoustic sum rule')
        self.Acoustic_sum_rulettk.pack(side='top')
        self.frameAcoustic_sum_rule.configure(height='200', width='200')
        self.frameAcoustic_sum_rule.pack(side='top')
        
        self.Phononframe.configure(height='200', text='Phonon Calculation Parameters', width='200')
        self.Phononframe.pack(side='left')
        # End Phononframe ------------------------------------------

        # labelframe4: Frame for Cell relaxation ----------------------
        self.frame13 = ttk.Frame(self.frame4)
        self.labelframe4 = ttk.Labelframe(self.frame13)
        self.frame22 = ttk.Frame(self.labelframe4)
        self.EpsXttk = ttk.Checkbutton(self.frame22)
        EpsXvar = BooleanVar()
        self.EpsXttk.configure(variable = EpsXvar, onvalue=True, offvalue=False, text='EpsX')
        self.EpsXttk.pack(side='top')
        self.EpsYttk = ttk.Checkbutton(self.frame22)
        EpsYvar = BooleanVar()
        self.EpsYttk.configure(variable = EpsYvar, onvalue=True, offvalue=False, text='EpsY')
        self.EpsYttk.pack(side='top')
        self.EpsZttk = ttk.Checkbutton(self.frame22)
        EpsZvar = BooleanVar()
        self.EpsZttk.configure(variable = EpsZvar, onvalue=True, offvalue=False, text='EpsZ')
        self.EpsZttk.pack(side='top')
        self.ShearYZttk = ttk.Checkbutton(self.frame22)
        ShearYZvar = BooleanVar()
        self.ShearYZttk.configure(variable = ShearYZvar, onvalue=True, offvalue=False, text='ShearYZ')
        self.ShearYZttk.pack(side='top')
        self.ShearXZttk = ttk.Checkbutton(self.frame22)
        ShearXZvar = BooleanVar()
        self.ShearXZttk.configure(variable = ShearXZvar, onvalue=True, offvalue=False, text='ShearXZ')
        self.ShearXZttk.pack(side='top')
        self.ShearXYttk = ttk.Checkbutton(self.frame22)
        ShearXYvar = BooleanVar()
        self.ShearXYttk.configure(variable = ShearXYvar, onvalue=True, offvalue=False, text='ShearXY')
        self.ShearXYttk.pack(side='top')
        self.frame22.configure(height='200', width='200')
        self.frame22.pack(side='top')
        self.labelframe4.configure(height='200', text='Cell Relaxation (Geometric Optim. must be selected)', width='200')
        self.labelframe4.pack(side='left')
        # End labelframe4 ------------------------------------------------
        
        # GWframe: Frame for GW parameters -------------------------------
        self.GWframe = ttk.Frame(self.frame4)
        self.labelGWframe = ttk.Labelframe(self.GWframe)

        # GWtype
        self.frameGW_calc_type = ttk.Frame(self.labelGWframe)
        self.labelGW_calc_type = ttk.Label(self.frameGW_calc_type)
        self.labelGW_calc_type.configure(text='GW calc type')
        self.labelGW_calc_type.pack(side='left')
        self.GW_calc_typettk = ttk.Combobox(self.frameGW_calc_type)
        self.GW_calc_typettk.configure(values=('GW0', 'G0W0'), state='readonly')
        self.GW_calc_typettk.pack(side='top')
        self.GW_calc_typettk.current(0)
        self.frameGW_calc_type.configure(height='200', width='200')
        self.frameGW_calc_type.pack(side='top')

        # GW_kpoints_list
        self.frameGW_kpoints_list = ttk.Frame(self.labelGWframe)
        self.labelGW_kpoints_list = ttk.Label(self.frameGW_kpoints_list)
        self.labelGW_kpoints_list.configure(text='GW K-points change as list [[kix,kiy,kiz],...]')
        self.labelGW_kpoints_list.pack(side='left')
        self.GW_kpoints_listttk = tk.Entry(self.frameGW_kpoints_list)
        self.GW_kpoints_listttk.delete('0', 'end')
        self.GW_kpoints_listttk.insert('0', '[[0.0,0.0,0.0]]')
        self.GW_kpoints_listttk.pack(side='top')
        self.frameGW_kpoints_list.configure(height='200', width='200')
        self.frameGW_kpoints_list.pack(side='top')

        # GW_truncation
        self.frameGW_truncation = ttk.Frame(self.labelGWframe)
        self.labelGW_truncation = ttk.Label(self.frameGW_truncation)
        self.labelGW_truncation.configure(text='GW truncation')
        self.labelGW_truncation.pack(side='left')
        self.GW_truncationttk = ttk.Combobox(self.frameGW_truncation)
        self.GW_truncationttk.configure(values=(None, '2D', '1D', '0D', 'wigner-seitz'), state='readonly')
        self.GW_truncationttk.pack(side='top')
        self.GW_truncationttk.current(4)
        self.frameGW_truncation.configure(height='200', width='200')
        self.frameGW_truncation.pack(side='top')

        # GW_cut_off_energy
        self.frameGW_cut_off_energy = ttk.Frame(self.labelGWframe)
        self.labelGW_cut_off_energy = ttk.Label(self.frameGW_cut_off_energy)
        self.labelGW_cut_off_energy.configure(text='Cut-off en. for opt.')
        self.labelGW_cut_off_energy.pack(side='left')
        self.GW_cut_off_energyttk = ttk.Entry(self.frameGW_cut_off_energy)
        self.GW_cut_off_energyttk.delete('0', 'end')
        self.GW_cut_off_energyttk.insert('0', '100')
        self.GW_cut_off_energyttk.pack(side='top')
        self.frameGW_cut_off_energy.configure(height='200', width='200')
        self.frameGW_cut_off_energy.pack(side='top')

        # GW_valence_band_no
        self.frameGW_valence_band_no = ttk.Frame(self.labelGWframe)
        self.labelGW_valence_band_no = ttk.Label(self.frameGW_valence_band_no)
        self.labelGW_valence_band_no.configure(text='Valence band number')
        self.labelGW_valence_band_no.pack(side='left')
        self.GW_valence_band_nottk = ttk.Entry(self.frameGW_valence_band_no)
        self.GW_valence_band_nottk.delete('0', 'end')
        self.GW_valence_band_nottk.insert('0', '8')
        self.GW_valence_band_nottk.pack(side='top')
        self.frameGW_valence_band_no.configure(height='200', width='200')
        self.frameGW_valence_band_no.pack(side='top')

        # GW_conduction_band_no
        self.frameGW_conduction_band_no = ttk.Frame(self.labelGWframe)
        self.labelGW_conduction_band_no = ttk.Label(self.frameGW_conduction_band_no)
        self.labelGW_conduction_band_no.configure(text='Conduction band number')
        self.labelGW_conduction_band_no.pack(side='left')
        self.GW_conduction_band_nottk = ttk.Entry(self.frameGW_conduction_band_no)
        self.GW_conduction_band_nottk.delete('0', 'end')
        self.GW_conduction_band_nottk.insert('0', '8')
        self.GW_conduction_band_nottk.pack(side='top')
        self.frameGW_conduction_band_no.configure(height='200', width='200')
        self.frameGW_conduction_band_no.pack(side='top')

        # GW_PPA
        self.GW_PPAttk = ttk.Checkbutton(self.labelGWframe)
        GW_PPAvar = BooleanVar()
        self.GW_PPAttk.configure(variable = GW_PPAvar, onvalue=True, offvalue=False, text='Plasmon Pole Approximation')
        self.GW_PPAttk.pack(side='top')

        # GW_q0_correction
        self.GW_q0_correctionttk = ttk.Checkbutton(self.labelGWframe)
        GW_q0_correctionvar = BooleanVar()
        self.GW_q0_correctionttk.configure(variable = GW_q0_correctionvar, onvalue=True, offvalue=False, text='Analytic correction to the q=0 contribution')
        self.GW_q0_correctionttk.pack(side='top')

        # GW_nblocks_max
        self.GW_nblocks_maxttk = ttk.Checkbutton(self.labelGWframe)
        GW_nblocks_maxvar = BooleanVar()
        self.GW_nblocks_maxttk.configure(variable = GW_nblocks_maxvar, onvalue=True, offvalue=False, text='Cuts chi0 into as many blocks to reduce mem.')
        self.GW_nblocks_maxttk.pack(side='top')

        # GW_interpolate_band
        self.GW_interpolate_bandttk = ttk.Checkbutton(self.labelGWframe)
        GW_interpolate_bandvar = BooleanVar()
        self.GW_interpolate_bandttk.configure(variable = GW_interpolate_bandvar, onvalue=True, offvalue=False, text='Spline draw for bands? (needs min. 3 points)')
        self.GW_interpolate_bandttk.pack(side='top')
        
        self.labelGWframe.configure(height='200', text='GW Parameters (Only applicable when Basis = PW-GW', width='200')
        self.labelGWframe.pack(side='left')
        self.GWframe.configure(height='200', width='200')
        self.GWframe.pack(side='left')
        # End GWframe ---------------------------------------------
        
        # labelframe5: Other Parameters ---------------------------
        self.labelframe5 = ttk.Labelframe(self.frame13)
     
        self.labelframe5.configure(height='200', text='General options', width='200')
        self.labelframe5.pack(side='top')
        self.frame13.configure(height='200', width='200')
        self.frame13.pack(side='left')
        self.frame4.configure(height='200', width='200')
        self.frame4.pack(side='top')
        
        # Maximum Energy
        self.frameEnergy_max = ttk.Frame(self.labelframe5)
        self.labelEnergy_max = ttk.Label(self.frameEnergy_max)
        self.labelEnergy_max.configure(text='Maximum energy in figures')
        self.labelEnergy_max.pack(side='left')
        self.Energy_maxttk = ttk.Entry(self.frameEnergy_max)
        self.Energy_maxttk.delete('0', 'end')
        self.Energy_maxttk.insert('0', '5')
        self.Energy_maxttk.pack(side='top')
        self.frameEnergy_max.configure(height='200', width='200')
        self.frameEnergy_max.pack(side='top')
        
        # Minimum Energy
        self.frameEnergy_min = ttk.Frame(self.labelframe5)
        self.labelEnergy_min = ttk.Label(self.frameEnergy_min)
        self.labelEnergy_min.configure(text='Minimum energy in figures')
        self.labelEnergy_min.pack(side='left')
        self.Energy_minttk = ttk.Entry(self.frameEnergy_min)
        self.Energy_minttk.delete('0', 'end')
        self.Energy_minttk.insert('0', '-5')
        self.Energy_minttk.pack(side='top')
        self.frameEnergy_min.configure(height='200', width='200')
        self.frameEnergy_min.pack(side='top')
        # End labelframe5 -------------------------------------------
        
        self.notebookUpper.add(self.frame4, state='normal', text='Input Parameters')
        
        # ------------- Calculate tab -----------------
        self.frame3 = ttk.Frame(self.notebookUpper)
        
        # MPI core number
        self.frame25 = ttk.Frame(self.frame3)
        self.label21 = ttk.Label(self.frame25)
        self.label21.configure(text='MPI core number')
        self.label21.pack(side='left')
        self.MPI_coresttk = ttk.Entry(self.frame25)
        self.MPI_coresttk.delete('0', 'end')
        self.MPI_coresttk.insert('0', '1')
        self.MPI_coresttk.pack(side='top')
        self.frame25.configure(height='200', width='200')
        self.frame25.pack(side='top')
        
        # Start calculation
        self.frame26 = ttk.Frame(self.frame3)
        self.button3 = ttk.Button(self.frame26)
        self.button3.configure(text='Start calculation')
        self.button3.pack(side='top')
        self.button3.configure(command=onCalculate)
        self.frame26.configure(height='200', width='200')
        self.frame26.pack(side='top')
        
        # Log text box
        self.frame27 = ttk.Frame(self.frame3)
        self.text4 = tk.Text(self.frame27)
        self.text4.configure(height='50', width='120')
        self.text4.insert('0.0', 'gpawsolve.py stdout log: \n')
        self.text4.pack(side='top')
        self.frame27.configure(height='200', width='200')
        self.frame27.pack(side='top')
        
        self.frame3.configure(height='200', width='200')
        self.frame3.pack(side='top')
        self.notebookUpper.add(self.frame3, text='Calculate')

        # --------------- About box -------------------
        self.frame24 = ttk.Frame(self.notebookUpper)
        self.text2 = tk.Text(self.frame24)
        self.text2.configure(background='#4f4f4f', foreground='#ffffff', height='14', undo='false')
        self.text2.configure(width='60', wrap='char')
        _text_ = '''GG (gpaw-tools & gui)
=======================
GG is a graphical user interface (GUI) for a 
gpawsolve.py script, which aims simple and
expediting calculations with GPAW/ASE codes.

For licensing information, please refer to LICENSE file.'''
        self.text2.insert('0.0', _text_)
        self.text2.pack(side='left')
        self.button1 = ttk.Button(self.frame24, text='gpaw-tools website', command=lambda aurl=url:OpenUrl(aurl))
        self.gg_fullsmall_png = tk.PhotoImage(file=os.path.join(PROJECT_PATH,'gui_files/gpaw-tools.png'))
        self.button1.configure(image=self.gg_fullsmall_png, state='normal')
        self.button1.pack(side='left')
        self.frame24.configure(height='200', width='1200')
        self.frame24.pack(side='top')
        self.notebookUpper.add(self.frame24, text='About')
        self.notebookUpper.configure(height='700', width='1500')
        self.notebookUpper.pack(fill='x', side='top')
        
        # Message log
        self.notebookBottom = ttk.Notebook(self.frame2)
        self.text1 = tk.Text(self.notebookBottom)
        self.text1.configure(background='#000000', foreground='#ffffff', height='10', width='50')
        _text_ = '''Program started.\n'''
        self.text1.insert('0.0', _text_)
        self.text1.pack(side='top')
        self.notebookBottom.add(self.text1, text='Message Log')
        self.notebookBottom.configure(height='100', width='1500')
        self.notebookBottom.pack(fill='x', side='top')
        self.frame2.configure(height='1000', width='1500')
        self.frame2.pack(fill='both', side='top')
        self.gg_png = tk.PhotoImage(file=os.path.join(PROJECT_PATH,'gui_files/gpaw-tools.png'))
        self.toplevel1.configure(height='1000', width='1500')
        self.toplevel1.iconphoto(True, self.gg_png)
        self.toplevel1.resizable(False, False)
        self.toplevel1.title('gpaw-tools GUI')

        # Main widget
        self.mainwindow = self.toplevel1


    def run(self):
        '''Running the mainloop'''
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = gg()
    app.run()
