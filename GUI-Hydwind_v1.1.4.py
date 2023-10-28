from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QGridLayout, QLabel, QGroupBox, QRadioButton, QWidget, QLineEdit, QCheckBox, QRadioButton, QVBoxLayout, QHBoxLayout, QScrollArea, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from subprocess import call, Popen
from os import chdir, getcwd
import sys, string, os, math, shutil, time
import fileinput
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
import matplotlib.patches as patches
import matplotlib.pyplot as pl
from scipy.interpolate import interp1d
import glob

#############      #      #############
#                                     #
#         Hydwind GUI v1.1.4          #
#     by Alonso Guerrero Caneppa      #
#    alonso.guerrero@alumnos.uv.cl    #
#            March 16, 2021           #
#      Universidad de Valparaiso      #
#                                     #
#############      #      #############
                   
class Prompt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(200)
        self.setFixedWidth(700)
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)

        welcome = QLabel('<b><u>Welcome to Hydwind GUI v1.1.4</u><b>')
        skeleton_layout.addWidget(welcome, alignment=Qt.AlignCenter)
        credits = QLabel('<b><i>by Alonso Guerrero C.</i></b>')
        skeleton_layout.addWidget(credits, alignment=Qt.AlignCenter)
        skeleton_layout.addWidget(QLabel(' ')) #para hacer espacio
        label_prompt = QLabel('Please select the method in which the parameters will be inputted:')
        skeleton_layout.addWidget(label_prompt, alignment=Qt.AlignCenter)
        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        buttons.setLayout(buttons_layout)
        skeleton_layout.addWidget(buttons, alignment=Qt.AlignCenter)
        manually = QPushButton('Manually', minimumWidth = 90, toolTip = 'Manually input parameters by filling required fields.') #Lo definimos como atributo (.self) de Prompt porque este boton sera llamado desde fuera de la Class.
        buttons_layout.addWidget(manually)
        from_text_file = QPushButton('From for011.dat file', minimumWidth = 160, toolTip = 'Automatically load parameters from formatted <i>for011.dat</i> text file (not available in this version).', enabled = False )
        buttons_layout.addWidget(from_text_file)
        
        def run():
            global Hydwind_Window
            Hydwind_Window = Window()
            self.close()

        manually.clicked.connect(run)    

        self.show()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedSize(700, 600)
        skeleton = QWidget() #Widget que sera el Central
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)

        #Creo las pestañas
        
        tabs = QTabWidget() #Para hacer pestañitas
        tab_general = QWidget() #Pestaña de ajustes Generales
        tab_general_layout = QVBoxLayout() #Su layout padre
        scroll_general = QScrollArea(widgetResizable=True)
        scroll_general.setWidget(tab_general)
        tab_general.setLayout(tab_general_layout)
        tab_advanced = QWidget() #Pestaña de ajustes Avanzados
        tab_advanced_layout = QVBoxLayout()
        scroll_advanced = QScrollArea(widgetResizable=True)
        scroll_advanced.setWidget(tab_advanced)
        tab_advanced.setLayout(tab_advanced_layout)
        tabs.addTab(scroll_general, "General Settings")
        tabs.addTab(scroll_advanced, "Advanced Settings")
        skeleton_layout.addWidget(tabs)
   
        ###GENERAL SETTINGS:###

        ###PRIMERA SECCION: MODEL NAME###

        section_model_name = QGroupBox()
        section_model_name_layout = QVBoxLayout()
        section_model_name.setLayout(section_model_name_layout)
        tab_general_layout.addWidget(section_model_name)

        section_model_name_A = QWidget()
        section_model_name_A_layout = QHBoxLayout()
        section_model_name_A.setLayout(section_model_name_A_layout)
        section_model_name_layout.addWidget(section_model_name_A)
        label_model_name = QLabel('Model name:')
        global model_name
        model_name = QLineEdit()
        section_model_name_A_layout.addWidget(label_model_name)
        section_model_name_A_layout.addWidget(model_name)
        section_model_name_A_layout.addWidget(QLabel(' ')) #Para hacer espacio

        prepend_model_name = QCheckBox("Prepend model name to output files' names")
        section_model_name_A_layout.addWidget(prepend_model_name)

        name_warning = QLabel('                    (Model name must not contain spaces)')
        section_model_name_layout.addWidget(name_warning)

        ###SEGUNDA SECCION: AUTOFILL EXAMPLES###

        seccion_autofill_examples = QGroupBox('AUTOFILL EXAMPLES')
        seccion_autofill_examples_layout = QVBoxLayout()
        seccion_autofill_examples.setLayout(seccion_autofill_examples_layout)
        tab_general_layout.addWidget(seccion_autofill_examples)
    
        autofill = QCheckBox("Autofill fields with example model's data")
        seccion_autofill_examples_layout.addWidget(autofill, alignment=Qt.AlignCenter)
        
        label_autofill = QLabel("Select an example model:")
        label_autofill.setDisabled(True)
        seccion_autofill_examples_layout.addWidget(label_autofill)

        autofill_models = QWidget()
        autofill_models_layout = QHBoxLayout()
        autofill_models.setLayout(autofill_models_layout)
        seccion_autofill_examples_layout.addWidget(autofill_models)
        button_autofill_delta_slow = QRadioButton('\u03b4-slow')
        button_autofill_delta_slow.setDisabled(True)
        autofill_models_layout.addWidget(button_autofill_delta_slow, alignment=Qt.AlignCenter)
        button_autofill_fast = QRadioButton('Fast')
        button_autofill_fast.setDisabled(True)
        autofill_models_layout.addWidget(button_autofill_fast, alignment=Qt.AlignCenter)
        button_autofill_fast_2 = QRadioButton('Fast-2')
        button_autofill_fast_2.setDisabled(True)
        autofill_models_layout.addWidget(button_autofill_fast_2, alignment=Qt.AlignCenter)
        button_autofill_omega_slow = QRadioButton('\u03a9-slow')
        button_autofill_omega_slow.setDisabled(True)
        autofill_models_layout.addWidget(button_autofill_omega_slow, alignment=Qt.AlignCenter)

        autofill_apply = QPushButton('Apply')
        autofill_apply.setDisabled(True)
        autofill_apply.setMaximumWidth(70)
        seccion_autofill_examples_layout.addWidget(autofill_apply, alignment=Qt.AlignCenter)

        def toggle_autofill_examples():
            if autofill.isChecked() == True:
                label_autofill.setDisabled(False)
                button_autofill_delta_slow.setDisabled(False)
                button_autofill_fast.setDisabled(False)
                button_autofill_fast_2.setDisabled(False)
                button_autofill_omega_slow.setDisabled(False)
                autofill_apply.setDisabled(False)

            else:
                label_autofill.setDisabled(True)
                button_autofill_delta_slow.setDisabled(True)
                button_autofill_fast.setDisabled(True)
                button_autofill_fast_2.setDisabled(True)
                button_autofill_omega_slow.setDisabled(True)
                autofill_apply.setDisabled(True)

        autofill.toggled.connect(toggle_autofill_examples)

        #INFO:

        double_precision = QLabel('<b><u>INFO:</u> All fields below allow double precision notation </b> (example: 2.0d65)')
        tab_general_layout.addWidget(double_precision, alignment=Qt.AlignCenter)
        tab_general_layout.addWidget(QLabel(' ')) #Para hacer espacio

        ###TERCERA SECCION: STELLAR PARAMETERS###

        seccion_stellar_parameters = QGroupBox('STELLAR PARAMETERS')
        seccion_stellar_parameters_layout = QVBoxLayout()
        seccion_stellar_parameters.setLayout(seccion_stellar_parameters_layout)
        tab_general_layout.addWidget(seccion_stellar_parameters)

        seccion_stellar_parameters_A = QWidget()
        seccion_stellar_parameters_A_layout = QHBoxLayout()
        seccion_stellar_parameters_A.setLayout(seccion_stellar_parameters_A_layout)
        seccion_stellar_parameters_layout.addWidget(seccion_stellar_parameters_A)

        label_effective_temperature = QLabel('Effective Temperature (in [K]):')
        effective_temperature = QLineEdit()
        seccion_stellar_parameters_A_layout.addWidget(label_effective_temperature)
        seccion_stellar_parameters_A_layout.addWidget(effective_temperature)
        label_stellar_radius = QLabel('Stellar Radius (in Solar Units):')
        stellar_radius = QLineEdit()
        seccion_stellar_parameters_A_layout.addWidget(label_stellar_radius)
        seccion_stellar_parameters_A_layout.addWidget(stellar_radius)

        seccion_stellar_parameters_B = QWidget()
        seccion_stellar_parameters_B_layout = QHBoxLayout()
        seccion_stellar_parameters_B.setLayout(seccion_stellar_parameters_B_layout)
        seccion_stellar_parameters_layout.addWidget(seccion_stellar_parameters_B)

        label_superficial_gravity = QLabel('Superficial Gravity (log(g)):')
        superficial_gravity = QLineEdit()
        seccion_stellar_parameters_B_layout.addWidget(label_superficial_gravity)
        seccion_stellar_parameters_B_layout.addWidget(superficial_gravity)
        label_angular_velocity = QLabel('Normalised Stellar Angular Velocity:')
        angular_velocity = QLineEdit()
        seccion_stellar_parameters_B_layout.addWidget(label_angular_velocity)
        seccion_stellar_parameters_B_layout.addWidget(angular_velocity)

        seccion_stellar_parameters_C = QWidget()
        seccion_stellar_parameters_C_layout = QHBoxLayout()
        seccion_stellar_parameters_C.setLayout(seccion_stellar_parameters_C_layout)
        seccion_stellar_parameters_layout.addWidget(seccion_stellar_parameters_C, alignment=Qt.AlignLeft)

        label_helium_abundance = QLabel('Helium Abundance relative to Hydrogen:')
        helium_abundance = QLineEdit(maximumWidth=100)
        seccion_stellar_parameters_C_layout.addWidget(label_helium_abundance, alignment=Qt.AlignRight)
        seccion_stellar_parameters_C_layout.addWidget(helium_abundance, alignment=Qt.AlignLeft)

        ###CUARTA SECCION: LINE-FORCE PARAMETERS:###

        seccion_line_force = QGroupBox('LINE-FORCE PARAMETERS')
        seccion_line_force_layout = QHBoxLayout()
        seccion_line_force.setLayout(seccion_line_force_layout)
        tab_general_layout.addWidget(seccion_line_force)

        label_k = QLabel('k:')
        k = QLineEdit(maximumWidth = 100)
        seccion_line_force_layout.addWidget(label_k, alignment=Qt.AlignRight)
        seccion_line_force_layout.addWidget(k, alignment=Qt.AlignLeft)
        seccion_line_force_layout.addWidget(QLabel(' ')) #para hacer espacio
        label_alpha = QLabel('\u03b1'+':')
        alpha = QLineEdit(maximumWidth = 100)
        seccion_line_force_layout.addWidget(label_alpha, alignment=Qt.AlignRight)
        seccion_line_force_layout.addWidget(alpha, alignment=Qt.AlignLeft)
        seccion_line_force_layout.addWidget(QLabel(' ')) #para hacer espacio
        label_delta = QLabel('\u03b4'+':')
        delta = QLineEdit(maximumWidth = 100)
        seccion_line_force_layout.addWidget(label_delta, alignment=Qt.AlignRight)
        seccion_line_force_layout.addWidget(delta, alignment=Qt.AlignLeft)
        seccion_line_force_layout.addWidget(QLabel(' ')) #para hacer espacio

        ###QUINTA SECCION: TRIAL VELOCITY PROFILE###

        seccion_trial_velocity_profile = QGroupBox('TRIAL VELOCITY PROFILE')
        seccion_trial_velocity_profile_layout = QVBoxLayout()
        seccion_trial_velocity_profile.setLayout(seccion_trial_velocity_profile_layout)
        tab_general_layout.addWidget(seccion_trial_velocity_profile)

        label_trial_velocity = QLabel('Trial Velocity Profile (hover cursor over options for more information):')
        seccion_trial_velocity_profile_layout.addWidget(label_trial_velocity)
                
        seccion_trial_velocity_profile_A = QWidget()
        seccion_trial_velocity_profile_A_layout = QHBoxLayout()
        seccion_trial_velocity_profile_A.setLayout(seccion_trial_velocity_profile_A_layout)
        seccion_trial_velocity_profile_layout.addWidget(seccion_trial_velocity_profile_A)
        button_trial_velocity_acc = QRadioButton('acc')
        button_trial_velocity_acc.setToolTip('Velocity profile obtained from an analytical expression based the work of Araya et al. (2014) (works with fast solutions and 0.0 <span>&#8818;</span> \u03b4 <span>&#8818;</span> 0.3)')
        seccion_trial_velocity_profile_A_layout.addWidget(button_trial_velocity_acc)
        button_trial_velocity_fast = QRadioButton('fast')
        button_trial_velocity_fast.setToolTip('Velocity profile based on a \u03B2-law, with \u03B2 = 0.8. v<sub>&#8734;</sub> is calculated based on Friend & Abbott (1986) and the eigenvalue is obtained from CAK theory.')
        seccion_trial_velocity_profile_A_layout.addWidget(button_trial_velocity_fast)
        button_trial_velocity_blaw = QRadioButton('Based on \u03B2-law')
        button_trial_velocity_blaw.setToolTip('Velocity profile based on a \u03B2-law (requires manual input in fields below).')
        seccion_trial_velocity_profile_A_layout.addWidget(button_trial_velocity_blaw)
        button_trial_velocity_dslow = QRadioButton('\u03b4-slow (not available in this version)')
        button_trial_velocity_dslow.setDisabled(True)
        button_trial_velocity_dslow.setToolTip('Velocity profile obtained from an analytical expression for \u03b4-slow solutions.')
        seccion_trial_velocity_profile_A_layout.addWidget(button_trial_velocity_dslow)

        b_law_information = QLabel("If 'Based on \u03B2-law' is selected, fill the fields below:")
        seccion_trial_velocity_profile_layout.addWidget(b_law_information, alignment=Qt.AlignCenter)

        seccion_trial_velocity_profile_B = QWidget()
        seccion_trial_velocity_profile_B_layout = QGridLayout()
        seccion_trial_velocity_profile_B.setLayout(seccion_trial_velocity_profile_B_layout)
        seccion_trial_velocity_profile_layout.addWidget(seccion_trial_velocity_profile_B)
        label_b_value = QLabel('\u03B2-value:')
        label_b_value.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(label_b_value, 0, 0, alignment=Qt.AlignCenter)
        seccion_trial_velocity_profile_B_layout.addWidget(QLabel(' '), 0, 1) #para hacer espacio
        b_value = QLineEdit()
        b_value.setMaximumWidth(100)
        b_value.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(b_value, 1, 0, alignment=Qt.AlignCenter)
        label_hyperbolic_excess_speed = QLabel('Escape Velocity (in [km/s]):')
        label_hyperbolic_excess_speed.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(label_hyperbolic_excess_speed, 0, 2, alignment=Qt.AlignCenter)
        seccion_trial_velocity_profile_B_layout.addWidget(QLabel(' '), 0, 3) #para hacer espacio
        hyperbolic_excess_speed = QLineEdit()
        hyperbolic_excess_speed.setMaximumWidth(100)
        hyperbolic_excess_speed.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(hyperbolic_excess_speed, 1, 2, alignment=Qt.AlignCenter)
        label_eigenvalue = QLabel('Eigenvalue:', toolTip = 'Usually around 50 to 150.')
        label_eigenvalue.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(label_eigenvalue, 0, 4, alignment=Qt.AlignCenter)
        eigenvalue = QLineEdit(toolTip = 'Usually around 50 to 150.')
        eigenvalue.setMaximumWidth(100)
        eigenvalue.setDisabled(True)
        seccion_trial_velocity_profile_B_layout.addWidget(eigenvalue, 1, 4,  alignment=Qt.AlignCenter)

        def toggle_b_parameters():
            if button_trial_velocity_blaw.isChecked() == True:
                label_b_value.setDisabled(False)
                b_value.setDisabled(False)
                label_hyperbolic_excess_speed.setDisabled(False)
                hyperbolic_excess_speed.setDisabled(False)
                label_eigenvalue.setDisabled(False)
                eigenvalue.setDisabled(False)
            else:
                label_b_value.setDisabled(True)
                b_value.setText('')
                b_value.setDisabled(True)
                label_hyperbolic_excess_speed.setDisabled(True)
                hyperbolic_excess_speed.setText('')
                hyperbolic_excess_speed.setDisabled(True)
                label_eigenvalue.setDisabled(True)
                eigenvalue.setText('')
                eigenvalue.setDisabled(True)

        button_trial_velocity_blaw.toggled.connect(toggle_b_parameters)

        ###SEXTA SECCION: ADDITIONAL TRIAL VELOCITY PROFILES###

        seccion_additional_trial_velocity_profile = QGroupBox('ADDITIONAL TRIAL VELOCITY PROFILES')
        seccion_additional_trial_velocity_profile_layout = QVBoxLayout()
        seccion_additional_trial_velocity_profile.setLayout(seccion_additional_trial_velocity_profile_layout)
        tab_general_layout.addWidget(seccion_additional_trial_velocity_profile)

        try_additional_trial_velocity = QCheckBox('Try additional Trial Velocity Profiles if the previous one fails to converge')
        seccion_additional_trial_velocity_profile_layout.addWidget(try_additional_trial_velocity, alignment=Qt.AlignCenter)

        seccion_additional_trial_velocity_profile_A = QWidget()
        seccion_additional_trial_velocity_profile_A_layout = QHBoxLayout()
        seccion_additional_trial_velocity_profile_A.setLayout(seccion_additional_trial_velocity_profile_A_layout)
        seccion_additional_trial_velocity_profile_layout.addWidget(seccion_additional_trial_velocity_profile_A)
        label_number_of_trials = QLabel('Amount of additional Trial Velocity Profiles:')
        label_number_of_trials.setDisabled(True)
        seccion_additional_trial_velocity_profile_A_layout.addWidget(label_number_of_trials)
        number_of_trials = QLineEdit()
        number_of_trials.setFixedWidth(100)
        number_of_trials.setDisabled(True)
        seccion_additional_trial_velocity_profile_A_layout.addWidget(number_of_trials, alignment=Qt.AlignLeft)
        confirm_number_of_trials = QPushButton('Confirm amount')
        confirm_number_of_trials.setFixedWidth(120)
        confirm_number_of_trials.setDisabled(True)
        seccion_additional_trial_velocity_profile_A_layout.addWidget(confirm_number_of_trials)
        clear_trials = QPushButton('Clear profiles')
        clear_trials.setFixedWidth(100)
        clear_trials.setDisabled(True)
        seccion_additional_trial_velocity_profile_A_layout.addWidget(clear_trials)
        
        Window.all_additional_trial_velocity_profiles = QWidget()

        def create_additional_trial_velocity_profiles():
            Window.all_additional_trial_velocity_profiles.setParent(None)
            Window.INPUT_number_of_trials = int(number_of_trials.text())
            Window.all_additional_trial_velocity_profiles = QWidget()
            Window.all_additional_trial_velocity_profiles_layout = QVBoxLayout()
            Window.all_additional_trial_velocity_profiles.setLayout(Window.all_additional_trial_velocity_profiles_layout)
            seccion_additional_trial_velocity_profile_layout.addWidget(Window.all_additional_trial_velocity_profiles)

            for i in range(1, Window.INPUT_number_of_trials+1):

                exec("Window.name_of_trial_"+str(i)+" = QLabel('<b>Additional Trial Velocity Profile </b>'+'<b>("+str(i)+")</b>')")
                exec("Window.all_additional_trial_velocity_profiles_layout.addWidget(Window.name_of_trial_"+str(i)+", alignment=Qt.AlignCenter)")

                exec("Window.label_trial_velocity_"+str(i)+" = QLabel('Trial Velocity Profile (hover cursor over options for more information):')")
                exec("Window.all_additional_trial_velocity_profiles_layout.addWidget(Window.label_trial_velocity_"+str(i)+")")

                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+" = QWidget()")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout = QHBoxLayout()")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+".setLayout(Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout)")
                exec("Window.all_additional_trial_velocity_profiles_layout.addWidget(Window.all_additional_trial_velocity_profiles_A"+str(i)+")")
                exec("Window.button_trial_velocity_acc_"+str(i)+" = QRadioButton('acc')")
                exec("Window.button_trial_velocity_acc_"+str(i)+".setToolTip('Velocity profile obtained from an analytical expression based the work of Araya et al. (2014) (works with fast solutions and 0.0 <span>&#8818;</span> \u03b4 <span>&#8818;</span> 0.3)')")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout.addWidget(Window.button_trial_velocity_acc_"+str(i)+")")
                exec("Window.button_trial_velocity_fast_"+str(i)+" = QRadioButton('fast')")
                exec("Window.button_trial_velocity_fast_"+str(i)+".setToolTip('Velocity profile based on a \u03B2-law, with \u03B2 = 0.8. v<sub>&#8734;</sub> is calculated based on Friend & Abbott (1986) and the eigenvalue is obtained from CAK theory.')")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout.addWidget(Window.button_trial_velocity_fast_"+str(i)+")")
                exec("Window.button_trial_velocity_blaw_"+str(i)+" = QRadioButton('Based on \u03B2-law')")
                exec("Window.button_trial_velocity_blaw_"+str(i)+".setToolTip('Velocity profile based on a \u03B2-law (requires manual input in fields below).')")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout.addWidget(Window.button_trial_velocity_blaw_"+str(i)+")")
                exec("Window.button_trial_velocity_dslow_"+str(i)+" = QRadioButton('\u03b4-slow (not available in this version)')")
                exec("Window.button_trial_velocity_dslow_"+str(i)+".setDisabled(True)")
                exec("Window.button_trial_velocity_dslow_"+str(i)+".setToolTip('Velocity profile obtained from an analytical expression for \u03b4-slow solutions.')")
                exec("Window.all_additional_trial_velocity_profiles_A"+str(i)+"_layout.addWidget(Window.button_trial_velocity_dslow_"+str(i)+")")

                exec("Window.b_law_information_"+str(i)+" = QLabel(\"If 'Based on \u03B2-law' is selected, fill the fields below:\")")
                exec("Window.all_additional_trial_velocity_profiles_layout.addWidget(Window.b_law_information_"+str(i)+", alignment=Qt.AlignCenter)")

                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+" = QWidget()")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout = QGridLayout()")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+".setLayout(Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout)")
                exec("Window.all_additional_trial_velocity_profiles_layout.addWidget(Window.all_additional_trial_velocity_profiles_B"+str(i)+")")
                exec("Window.label_b_value_"+str(i)+" = QLabel('\u03B2-value:')")
                exec("Window.label_b_value_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.label_b_value_"+str(i)+", 0, 0, alignment=Qt.AlignCenter)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(QLabel(' '), 0, 1)") #para hacer espacio
                exec("Window.b_value_"+str(i)+" = QLineEdit()")
                exec("Window.b_value_"+str(i)+".setMaximumWidth(100)")
                exec("Window.b_value_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.b_value_"+str(i)+", 1, 0, alignment=Qt.AlignCenter)")
                exec("Window.label_hyperbolic_excess_speed_"+str(i)+" = QLabel('Escape Velocity (in [km/s]):')")
                exec("Window.label_hyperbolic_excess_speed_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.label_hyperbolic_excess_speed_"+str(i)+", 0, 2, alignment=Qt.AlignCenter)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(QLabel(' '), 0, 3)") #para hacer espacio
                exec("Window.hyperbolic_excess_speed_"+str(i)+" = QLineEdit()")
                exec("Window.hyperbolic_excess_speed_"+str(i)+".setMaximumWidth(100)")
                exec("Window.hyperbolic_excess_speed_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.hyperbolic_excess_speed_"+str(i)+", 1, 2, alignment=Qt.AlignCenter)")
                exec("Window.label_eigenvalue_"+str(i)+" = QLabel('Eigenvalue:', toolTip = 'Usually around 50 to 150.')")
                exec("Window.label_eigenvalue_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.label_eigenvalue_"+str(i)+", 0, 4, alignment=Qt.AlignCenter)")
                exec("Window.eigenvalue_"+str(i)+" = QLineEdit(toolTip = 'Usually around 50 to 150.')")
                exec("Window.eigenvalue_"+str(i)+".setMaximumWidth(100)")
                exec("Window.eigenvalue_"+str(i)+".setDisabled(True)")
                exec("Window.all_additional_trial_velocity_profiles_B"+str(i)+"_layout.addWidget(Window.eigenvalue_"+str(i)+", 1, 4,  alignment=Qt.AlignCenter)")
            
                exec("def toggle_b_parameters_"+str(i)+"():\n\tif Window.button_trial_velocity_blaw_"+str(i)+".isChecked() == True:\n\t\tWindow.label_b_value_"+str(i)+".setDisabled(False)\n\t\tWindow.b_value_"+str(i)+".setDisabled(False)\n\t\tWindow.label_hyperbolic_excess_speed_"+str(i)+".setDisabled(False)\n\t\tWindow.hyperbolic_excess_speed_"+str(i)+".setDisabled(False)\n\t\tWindow.label_eigenvalue_"+str(i)+".setDisabled(False)\n\t\tWindow.eigenvalue_"+str(i)+".setDisabled(False)\n\telse:\n\t\tWindow.label_b_value_"+str(i)+".setDisabled(True)\n\t\tWindow.b_value_"+str(i)+".setText('')\n\t\tWindow.b_value_"+str(i)+".setDisabled(True)\n\t\tWindow.label_hyperbolic_excess_speed_"+str(i)+".setDisabled(True)\n\t\tWindow.hyperbolic_excess_speed_"+str(i)+".setText('')\n\t\tWindow.hyperbolic_excess_speed_"+str(i)+".setDisabled(True)\n\t\tWindow.label_eigenvalue_"+str(i)+".setDisabled(True)\n\t\tWindow.eigenvalue_"+str(i)+".setText('')\n\t\tWindow.eigenvalue_"+str(i)+".setDisabled(True)")

                exec("Window.button_trial_velocity_blaw_"+str(i)+".toggled.connect(toggle_b_parameters_"+str(i)+")")
            
        def clear_profiles():
            Window.all_additional_trial_velocity_profiles.setParent(None)
            number_of_trials.setText('')

        clear_trials.clicked.connect(clear_profiles)
        confirm_number_of_trials.clicked.connect(create_additional_trial_velocity_profiles)
        
        def toggle_additional_trial_velocity_profiles():
            if try_additional_trial_velocity.isChecked() == True:
                label_number_of_trials.setDisabled(False)
                number_of_trials.setDisabled(False)
                confirm_number_of_trials.setDisabled(False)
                clear_trials.setDisabled(False)
            else:
                label_number_of_trials.setDisabled(True)
                number_of_trials.setText('')
                number_of_trials.setDisabled(True)
                confirm_number_of_trials.setDisabled(True)
                clear_trials.setDisabled(True)
                clear_profiles()

        try_additional_trial_velocity.toggled.connect(toggle_additional_trial_velocity_profiles)

        ###SEPTIMA SECCION: OUTPUT SETTINGS###

        seccion_output_settings = QGroupBox('OUTPUT SETTINGS')
        seccion_output_settings_layout = QVBoxLayout()
        seccion_output_settings.setLayout(seccion_output_settings_layout)
        tab_general_layout.addWidget(seccion_output_settings)

        save_output = QCheckBox("Save standard output as 'hydwind.out' file")
        seccion_output_settings_layout.addWidget(save_output)

        model_michel = QCheckBox("Generate optional 'model_name.michel' file (hove mouse for more information)")
        model_michel.setToolTip('File to be used as input for FASTWIND code.')
        seccion_output_settings_layout.addWidget(model_michel, alignment=Qt.AlignLeft)

        ###ADVANCED SETTINGS:###

        button_reset_default = QPushButton('Reset all fields below to default', minimumWidth=200) #DEFINIRE SU FUNCION AL FINAL
        tab_advanced_layout.addWidget(button_reset_default, alignment=Qt.AlignCenter)

        ###PRIMERA SECCION: FREE ELECTRONS:###

        seccion_free_electrons = QGroupBox('FREE ELECTRONS')
        seccion_free_electrons_layout = QVBoxLayout()
        seccion_free_electrons.setLayout(seccion_free_electrons_layout)
        tab_advanced_layout.addWidget(seccion_free_electrons)

        seccion_free_electrons_A = QWidget()
        seccion_free_electrons_A_layout = QHBoxLayout()
        seccion_free_electrons_A.setLayout(seccion_free_electrons_A_layout)
        seccion_free_electrons_layout.addWidget(seccion_free_electrons_A)

        label_free_electrons = QLabel('Number of free electrons provided by Helium (*):')
        seccion_free_electrons_A_layout.addWidget(label_free_electrons)
        button_free_electrons_0 = QRadioButton('0.0')
        button_free_electrons_1 = QRadioButton('1.0')
        button_free_electrons_2 = QRadioButton('2.0')
        seccion_free_electrons_A_layout.addWidget(button_free_electrons_0, alignment=Qt.AlignRight)
        seccion_free_electrons_A_layout.addWidget(button_free_electrons_1, alignment=Qt.AlignCenter)
        seccion_free_electrons_A_layout.addWidget(button_free_electrons_2, alignment=Qt.AlignLeft)
        
        info_free_electrons = QLabel('(*): Suggested option is automatically calculated (and selected) from the inputted value for Effective Temperature in General Settings.', wordWrap = True)
        seccion_free_electrons_layout.addWidget(info_free_electrons)

        def free_electrons_calculation():
            INPUT_effective_temperature = str(effective_temperature.text())
            if len(INPUT_effective_temperature)>0:
                if float(INPUT_effective_temperature.replace('d', 'e')) <= 13000:
                    button_free_electrons_0.setChecked(True)
                    button_free_electrons_1.setChecked(False)
                    button_free_electrons_2.setChecked(False)
                if float(INPUT_effective_temperature.replace('d', 'e')) > 13000 and float(INPUT_effective_temperature.replace('d', 'e')) <= 28000:
                    button_free_electrons_0.setChecked(False)
                    button_free_electrons_1.setChecked(True)
                    button_free_electrons_2.setChecked(False)
                if float(INPUT_effective_temperature.replace('d', 'e')) > 28000:
                    button_free_electrons_0.setChecked(False)
                    button_free_electrons_1.setChecked(False)
                    button_free_electrons_2.setChecked(True)
        
        effective_temperature.editingFinished.connect(free_electrons_calculation)
    
        ###SEGUNDA SECCION: COMPUTING PARAMETERS:###

        seccion_computing_parameters = QGroupBox('COMPUTING PARAMETERS')
        seccion_computing_parameters_layout = QVBoxLayout()
        seccion_computing_parameters.setLayout(seccion_computing_parameters_layout)
        tab_advanced_layout.addWidget(seccion_computing_parameters)

        computing_parameters_A = QWidget()
        computing_parameters_A_layout = QHBoxLayout()
        computing_parameters_A.setLayout(computing_parameters_A_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_A)
        label_theory = QLabel('Theory used for calculations:')
        button_PPK = QRadioButton('PPK', checked = True)
        button_CAK = QRadioButton('CAK')
        button_FA = QRadioButton('FA')
        computing_parameters_A_layout.addWidget(label_theory)
        computing_parameters_A_layout.addWidget(button_PPK, alignment=Qt.AlignRight)
        computing_parameters_A_layout.addWidget(button_CAK, alignment=Qt.AlignCenter)
        computing_parameters_A_layout.addWidget(button_FA, alignment=Qt.AlignLeft)
        
        oblate_factor = QCheckBox('Consider Oblate Factor effect')
        gravity_darkening = QCheckBox('Consider Gravity Darkening effect')

        computing_parameters_B = QWidget()
        computing_parameters_B_layout = QHBoxLayout()
        computing_parameters_B_layout.addWidget(oblate_factor)
        computing_parameters_B_layout.addWidget(gravity_darkening)
        computing_parameters_B.setLayout(computing_parameters_B_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_B)

        label_lower_boundary = QLabel('Lower Boundary condition:')
        button_optical_depth = QRadioButton('Optical Depth Integral', checked=True)
        button_surface_mass = QRadioButton('Surface Mass Density')

        computing_parameters_C = QWidget()
        computing_parameters_C_layout = QGridLayout()
        computing_parameters_C_layout.addWidget(label_lower_boundary, 0, 0)
        computing_parameters_C_layout.addWidget(button_optical_depth, 0, 1)
        computing_parameters_C_layout.addWidget(button_surface_mass, 1, 1)
        computing_parameters_C_layout.addWidget(QWidget(), 0, 2) #Para hacer espacio
        computing_parameters_C_layout.addWidget(QWidget(), 0, 3) #Para hacer mas espacio
        computing_parameters_C.setLayout(computing_parameters_C_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_C)

        label_value_lower_boundary = QLabel('Value of selected Lower Boundary condition (in [cgs] units):')
        value_lower_boundary = QLineEdit('0.66667d0', maximumWidth=100)

        label_integration_method = QLabel('Integration method to use:')
        button_spline = QRadioButton('Spline', checked=True)
        button_trapezoidal = QRadioButton('Trapezoidal')
        computing_parameters_D = QWidget()
        computing_parameters_D_layout = QHBoxLayout()
        computing_parameters_D_layout.addWidget(label_integration_method, alignment=Qt.AlignRight)
        computing_parameters_D_layout.addWidget(button_spline, alignment=Qt.AlignRight)
        computing_parameters_D_layout.addWidget(button_trapezoidal, alignment=Qt.AlignLeft)
        computing_parameters_D.setLayout(computing_parameters_D_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_D, alignment=Qt.AlignLeft)

        def toggle_integration():
            if button_optical_depth.isChecked() == True:
                label_integration_method.setDisabled(False)
                button_spline.setDisabled(False)
                button_spline.setChecked(True)
                button_trapezoidal.setDisabled(False)
            if button_optical_depth.isChecked() == False:
                label_integration_method.setDisabled(True)
                button_spline.setDisabled(True)
                button_spline.setChecked(False)
                button_trapezoidal.setDisabled(True)
                button_trapezoidal.setChecked(False)

        button_optical_depth.toggled.connect(toggle_integration)

        computing_parameters_E = QWidget()
        computing_parameters_E_layout = QHBoxLayout()
        computing_parameters_E_layout.addWidget(label_value_lower_boundary, alignment=Qt.AlignRight)
        computing_parameters_E_layout.addWidget(value_lower_boundary)
        computing_parameters_E.setLayout(computing_parameters_E_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_E, alignment=Qt.AlignLeft)

        label_initial_zone_mesh = QLabel('Initial zone in the mesh (in stellar radius units):')
        initial_zone_mesh = QLineEdit('1', maximumWidth=100)
        label_last_zone_mesh = QLabel('Last zone in the mesh (in stellar radius units):')
        last_zone_mesh = QLineEdit('500', maximumWidth=100)

        computing_parameters_F = QWidget()
        computing_parameters_F_layout = QHBoxLayout()
        computing_parameters_F_layout.addWidget(label_initial_zone_mesh)
        computing_parameters_F_layout.addWidget(initial_zone_mesh)
        computing_parameters_F_layout.addWidget(QWidget()) # para hacer espacio
        computing_parameters_F.setLayout(computing_parameters_F_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_F)

        computing_parameters_G = QWidget()
        computing_parameters_G_layout = QHBoxLayout()
        computing_parameters_G_layout.addWidget(label_last_zone_mesh)
        computing_parameters_G_layout.addWidget(last_zone_mesh)
        computing_parameters_G_layout.addWidget(QWidget()) #para hacer espacio
        computing_parameters_G.setLayout(computing_parameters_G_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_G)

        label_number_mesh = QLabel('Number of zones in the mesh:')
        number_mesh = QLineEdit('200', maximumWidth=100)

        computing_parameters_H = QWidget()
        computing_parameters_H_layout = QHBoxLayout()
        computing_parameters_H_layout.addWidget(label_number_mesh)
        computing_parameters_H_layout.addWidget(number_mesh)
        computing_parameters_H_layout.addWidget(QWidget()) #para hacer espacio
        computing_parameters_H_layout.addWidget(QWidget()) #para hacer espacio
        computing_parameters_H.setLayout(computing_parameters_H_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_H)

        label_co_latitude_method = QLabel('Select the way in which the force inclinations will behave:')
        button_1d = QRadioButton('1-D', checked=True)
        button_15d = QRadioButton('1.5-D')
        
        computing_parameters_I = QWidget()
        computing_parameters_I_layout = QHBoxLayout()
        computing_parameters_I_layout.addWidget(label_co_latitude_method, alignment=Qt.AlignRight)
        computing_parameters_I_layout.addWidget(button_1d, alignment=Qt.AlignRight)
        computing_parameters_I_layout.addWidget(button_15d, alignment=Qt.AlignLeft)
        computing_parameters_I.setLayout(computing_parameters_I_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_I, alignment=Qt.AlignLeft)

        label_initial_co_latitude = QLabel('Initial Co-Latitude (in degrees):', enabled=False)
        initial_co_latitude = QLineEdit('90', maximumWidth=100, enabled=False)
        label_last_co_latitude = QLabel('Last Co-Latitude (in degrees):', enabled=False)
        last_co_latitude = QLineEdit('90', maximumWidth=100, enabled=False)
        label_steps_co_latitude = QLabel('Size of steps (in degrees):', enabled=False)
        steps_co_latitude = QLineEdit('0', maximumWidth=100, enabled=False)

        computing_parameters_J = QWidget()
        computing_parameters_J_layout = QGridLayout()
        computing_parameters_J_layout.addWidget(label_initial_co_latitude, 0, 0, alignment=Qt.AlignCenter)
        computing_parameters_J_layout.addWidget(initial_co_latitude, 1, 0, alignment=Qt.AlignCenter)
        computing_parameters_J_layout.addWidget(label_last_co_latitude, 0, 1, alignment=Qt.AlignCenter)
        computing_parameters_J_layout.addWidget(last_co_latitude, 1, 1, alignment=Qt.AlignCenter)
        computing_parameters_J_layout.addWidget(label_steps_co_latitude, 0, 2, alignment=Qt.AlignCenter)
        computing_parameters_J_layout.addWidget(steps_co_latitude, 1, 2, alignment=Qt.AlignCenter)
        computing_parameters_J.setLayout(computing_parameters_J_layout)
        seccion_computing_parameters_layout.addWidget(computing_parameters_J)

        def toggle_co_latitudes():
            if button_15d.isChecked() == True:
                label_initial_co_latitude.setDisabled(False)
                initial_co_latitude.setText('')
                initial_co_latitude.setDisabled(False)
                label_last_co_latitude.setDisabled(False)
                last_co_latitude.setText('')
                last_co_latitude.setDisabled(False)
                label_steps_co_latitude.setDisabled(False)
                steps_co_latitude.setText('')
                steps_co_latitude.setDisabled(False)
            else:
                label_initial_co_latitude.setDisabled(True)
                initial_co_latitude.setText('90')
                initial_co_latitude.setDisabled(True)
                last_co_latitude.setDisabled(True)
                last_co_latitude.setText('90')
                label_last_co_latitude.setDisabled(True)
                label_steps_co_latitude.setDisabled(True)
                steps_co_latitude.setText('0')
                steps_co_latitude.setDisabled(True)

        button_15d.toggled.connect(toggle_co_latitudes)
    
        ###TERCERA SECCION: COMPUTING CRITERIA###

        seccion_computing_criteria = QGroupBox('COMPUTING CRITERIA')
        seccion_computing_criteria_layout = QVBoxLayout()
        seccion_computing_criteria.setLayout(seccion_computing_criteria_layout)
        tab_advanced_layout.addWidget(seccion_computing_criteria)

        seccion_computing_criteria_A = QWidget()
        seccion_computing_criteria_A_layout = QGridLayout()
        seccion_computing_criteria_A.setLayout(seccion_computing_criteria_A_layout)
        seccion_computing_criteria_layout.addWidget(seccion_computing_criteria_A)
        label_convergence_criterion = QLabel('Convergence Criterion:')
        seccion_computing_criteria_A_layout.addWidget(label_convergence_criterion, 0, 0, alignment=Qt.AlignCenter)
        convergence_criterion = QLineEdit('1e-6')
        convergence_criterion.setMaximumWidth(100)
        seccion_computing_criteria_A_layout.addWidget(convergence_criterion, 1, 0, alignment=Qt.AlignCenter)
        seccion_computing_criteria_A_layout.addWidget(QWidget(), 0, 1, alignment=Qt.AlignCenter) #para hacer espacio 
        label_factor_corrections = QLabel('Factor of corrections applied after each iteration:')
        seccion_computing_criteria_A_layout.addWidget(label_factor_corrections, 0, 2, alignment=Qt.AlignCenter)
        factor_corrections = QLineEdit('1e-3')
        factor_corrections.setMaximumWidth(100)
        seccion_computing_criteria_A_layout.addWidget(factor_corrections, 1, 2, alignment=Qt.AlignCenter)
        
        seccion_computing_criteria_B = QWidget()
        seccion_computing_criteria_B_layout = QHBoxLayout()
        seccion_computing_criteria_B.setLayout(seccion_computing_criteria_B_layout)
        seccion_computing_criteria_layout.addWidget(seccion_computing_criteria_B)
        label_consider_v = QLabel('Consider v(R<sub>*</sub>) &lt; a :')
        seccion_computing_criteria_B_layout.addWidget(label_consider_v, alignment=Qt.AlignRight)
        consider_v = QCheckBox(checked=True)
        seccion_computing_criteria_B_layout.addWidget(consider_v, alignment=Qt.AlignLeft)

        ###CUARTA SECCION: DISCONTINUITY CHECKS IN DW/DU###

        seccion_discontinuity_checks = QGroupBox("DISCONTINUITY CHECKS IN 'dw/du'")
        seccion_discontinuity_checks_layout = QVBoxLayout()
        seccion_discontinuity_checks.setLayout(seccion_discontinuity_checks_layout)
        tab_advanced_layout.addWidget(seccion_discontinuity_checks)

        first_method = QCheckBox('Check discontinuity in dw/du (first method)', checked=True)
        seccion_discontinuity_checks_layout.addWidget(first_method, alignment=Qt.AlignLeft)

        second_method = QCheckBox('Check discontinuity in dw/du (second method)')
        seccion_discontinuity_checks_layout.addWidget(second_method, alignment=Qt.AlignLeft)

        third_method = QCheckBox('Check discontinuity in dw/du (third method)')
        seccion_discontinuity_checks_layout.addWidget(third_method, alignment=Qt.AlignLeft)

        ###DANDOLE FUNCION AL RETURN TO DEFAULT:

        def default_advanced_settings():
            button_PPK.setChecked(True)
            oblate_factor.setChecked(False)
            gravity_darkening.setChecked(False)
            button_optical_depth.setChecked(True)
            button_spline.setChecked(True)
            value_lower_boundary.setText('0.66667d0')
            initial_zone_mesh.setText('1')
            last_zone_mesh.setText('500')
            number_mesh.setText('200')
            button_1d.setChecked(True)
            convergence_criterion.setText('1e-6')
            factor_corrections.setText('1e-3')
            first_method.setChecked(True)
            second_method.setChecked(False)
            third_method.setChecked(False)

        button_reset_default.clicked.connect(free_electrons_calculation)
        button_reset_default.clicked.connect(default_advanced_settings)

            


        ###METODO PARA AUTOFILL DE EJEMPLOS### (si bien los botones de autofill estan al principio de la ventana, tengo que definirlos aqui
        #al final porque los "fields" a rellenar ya estan todos definidos en este punto. Por ende recien los puedo rellenar automaticamente)###

        def autofill_fields():

            ###DELTA SLOW:###

            if button_autofill_delta_slow.isChecked() == True:
                effective_temperature.setText('10000')
                stellar_radius.setText('60')
                helium_abundance.setText('0.1')
                superficial_gravity.setText('2.0')
                button_free_electrons_0.setChecked(True)
                angular_velocity.setText('0')
                k.setText('0.37')
                alpha.setText('0.49')
                delta.setText('0.3')
                button_PPK.setChecked(True)
                button_spline.setChecked(True)
                oblate_factor.setChecked(False)
                gravity_darkening.setChecked(False)
                button_surface_mass.setChecked(True)
                value_lower_boundary.setText('2.857d-11')
                initial_zone_mesh.setText('1')
                last_zone_mesh.setText('150')
                number_mesh.setText('900')
                button_1d.setChecked(True)
                convergence_criterion.setText('1e-6')
                factor_corrections.setText('1e-3')
                consider_v.setChecked(True)
                button_trial_velocity_blaw.setChecked(True)
                b_value.setText('3')
                hyperbolic_excess_speed.setText('200')
                eigenvalue.setText('90')
                try_additional_trial_velocity.setChecked(False)
                first_method.setChecked(True)
                second_method.setChecked(False)
                third_method.setChecked(False)
                save_output.setChecked(True)
                model_michel.setChecked(True)

            ###FAST:###

            if button_autofill_fast.isChecked() == True:
                effective_temperature.setText('30000.d0')
                stellar_radius.setText('29.d0')
                helium_abundance.setText('0.1')
                superficial_gravity.setText('3.45d0')
                button_free_electrons_2.setChecked(True)
                angular_velocity.setText('0')
                k.setText('0.17d0')
                alpha.setText('0.59d0')
                delta.setText('0.09d0')
                button_PPK.setChecked(True)
                button_spline.setChecked(True)
                oblate_factor.setChecked(False)
                gravity_darkening.setChecked(False)
                button_optical_depth.setChecked(True)
                value_lower_boundary.setText('0.66667d0')
                initial_zone_mesh.setText('1')
                last_zone_mesh.setText('100')
                number_mesh.setText('900')
                button_1d.setChecked(True)
                convergence_criterion.setText('1e-6')
                factor_corrections.setText('1e-3')
                consider_v.setChecked(True)
                button_trial_velocity_acc.setChecked(True)
                try_additional_trial_velocity.setChecked(False)
                first_method.setChecked(True)
                second_method.setChecked(False)
                third_method.setChecked(False)
                save_output.setChecked(True)
                model_michel.setChecked(True)       

            ###FAST 2:###

            if button_autofill_fast_2.isChecked() == True:
                effective_temperature.setText('17500.d0')
                stellar_radius.setText('49.d0')
                helium_abundance.setText('0.1')
                superficial_gravity.setText('2.7d0')
                button_free_electrons_1.setChecked(True)
                angular_velocity.setText('0')
                k.setText('0.57d0')
                alpha.setText('0.45d0')
                delta.setText('0.00d0')
                button_PPK.setChecked(True)
                button_spline.setChecked(True)
                oblate_factor.setChecked(False)
                gravity_darkening.setChecked(False)
                button_optical_depth.setChecked(True)
                value_lower_boundary.setText('0.66667d0')
                initial_zone_mesh.setText('1')
                last_zone_mesh.setText('200')
                number_mesh.setText('900')
                button_1d.setChecked(True)
                convergence_criterion.setText('1e-6')
                factor_corrections.setText('1e-3')
                consider_v.setChecked(True)
                button_trial_velocity_acc.setChecked(True)
                try_additional_trial_velocity.setChecked(True)
                number_of_trials.setText('1')
                confirm_number_of_trials.click()
                Window.button_trial_velocity_fast_1.setChecked(True)
                first_method.setChecked(True)
                second_method.setChecked(False)
                third_method.setChecked(False)
                save_output.setChecked(True)
                model_michel.setChecked(True)

            ###OMEGA SLOW:###

            if button_autofill_omega_slow.isChecked() == True:
                effective_temperature.setText('25000.')
                stellar_radius.setText('10.00')
                helium_abundance.setText('0.1')
                superficial_gravity.setText('3.5')
                button_free_electrons_1.setChecked(True)
                angular_velocity.setText('0.80')
                k.setText('0.32')
                alpha.setText('0.565')
                delta.setText('0.02')
                button_PPK.setChecked(True)
                button_spline.setChecked(True)
                oblate_factor.setChecked(False)
                gravity_darkening.setChecked(False)
                button_surface_mass.setChecked(True)
                value_lower_boundary.setText('5.d-11')
                initial_zone_mesh.setText('1')
                last_zone_mesh.setText('200')
                number_mesh.setText('900')
                button_1d.setChecked(True)
                convergence_criterion.setText('1e-6')
                factor_corrections.setText('1e-3')
                consider_v.setChecked(True)
                button_trial_velocity_fast.setChecked(True)
                try_additional_trial_velocity.setChecked(True)
                number_of_trials.setText('2')
                confirm_number_of_trials.click()
                Window.button_trial_velocity_blaw_1.setChecked(True)
                Window.b_value_1.setText('1.5')
                Window.hyperbolic_excess_speed_1.setText('1400.0')
                Window.eigenvalue_1.setText('30.0')
                Window.button_trial_velocity_blaw_2.setChecked(True)
                Window.b_value_2.setText('1.5')
                Window.hyperbolic_excess_speed_2.setText('400.0')
                Window.eigenvalue_2.setText('30.0')
                first_method.setChecked(True)
                second_method.setChecked(False)
                third_method.setChecked(False)
                save_output.setChecked(True)
                model_michel.setChecked(True)

        autofill_apply.clicked.connect(autofill_fields)

        ###BOTONES DE LA PARTE DE ABAJO###

        lower_buttons = QWidget()
        lower_buttons_layout = QHBoxLayout()
        lower_buttons.setLayout(lower_buttons_layout)
        skeleton_layout.addWidget(lower_buttons)

        go_back = QPushButton('Go back', maximumWidth = 70)
        lower_buttons_layout.addWidget(go_back, alignment=Qt.AlignLeft)

        def back():
            Hydwind_Prompt.show()
            Hydwind_Window.hide()

        go_back.clicked.connect(back)

        clear_fields = QPushButton('Clear all fields', minimumWidth=110)
        lower_buttons_layout.addWidget(clear_fields, alignment=Qt.AlignLeft)

        def clear_all_fields():
            autofill.setChecked(False)
            effective_temperature.setText('')
            stellar_radius.setText('')
            superficial_gravity.setText('')
            angular_velocity.setText('')
            helium_abundance.setText('')
            k.setText('')
            alpha.setText('')
            delta.setText('')
            button_trial_velocity_acc.setChecked(False)
            button_trial_velocity_fast.setChecked(False)
            button_trial_velocity_dslow.setChecked(False)
            button_trial_velocity_blaw.setChecked(False)
            try_additional_trial_velocity.setChecked(False)
            save_output.setChecked(False)
            model_michel.setChecked(False)
            button_free_electrons_0.setChecked(False)
            button_free_electrons_1.setChecked(False)
            button_free_electrons_2.setChecked(False)
            button_PPK.setChecked(False)
            button_CAK.setChecked(False)
            button_FA.setChecked(False)
            oblate_factor.setChecked(False)
            gravity_darkening.setChecked(False)
            button_optical_depth.setChecked(False)
            button_surface_mass.setChecked(False)
            value_lower_boundary.setText('')
            button_spline.setChecked(False)
            button_trapezoidal.setChecked(False)
            initial_zone_mesh.setText('')
            last_zone_mesh.setText('')
            number_mesh.setText('')
            button_1d.setChecked(False)
            button_15d.setChecked(False)
            initial_co_latitude.setText('')
            last_co_latitude.setText('')
            steps_co_latitude.setText('')
            convergence_criterion.setText('')
            factor_corrections.setText('')
            consider_v.setChecked(False)
            first_method.setChecked(False)
            second_method.setChecked(False)
            third_method.setChecked(False)
    
        clear_fields.clicked.connect(clear_all_fields)

        lower_buttons_layout.addWidget(QLabel('')) #Para hacer espacio
        lower_buttons_layout.addWidget(QLabel('')) #Para hacer espacio
        lower_buttons_layout.addWidget(QLabel('')) #Para hacer espacio
        lower_buttons_layout.addWidget(QLabel('')) #Para hacer espacio
        lower_buttons_layout.addWidget(QLabel('')) #Para hacer espacio

        button_run = QPushButton('Run', minimumWidth=50)
        lower_buttons_layout.addWidget(button_run, alignment=Qt.AlignRight)
        
        global original_path
        original_path = getcwd()
        def run_app():
    
            call(['mkdir', model_name.text()])
            chdir(original_path +'/'+model_name.text())
            for011 = open('for011.dat', 'w+')
            
            #PRIMERA LINEA

            for011.write('%s ' % (model_name.text()))
            
            if prepend_model_name.isChecked() == True:
                for011.write('T ')
            if prepend_model_name.isChecked() == False:
                for011.write('F ')
            
            if save_output.isChecked() == True:
                for011.write('T ')
            if save_output.isChecked() == False:
                for011.write('F ')

            if model_michel.isChecked() == True:
                for011.write('T\n')
            if model_michel.isChecked() == False:
                for011.write('F\n')

            #SEGUNDA LINEA

            for011.write('%s %s %s %s\n' % (effective_temperature.text(), superficial_gravity.text(), stellar_radius.text(), angular_velocity.text()))

            #TERCERA LINEA

            for011.write('%s %s %s\n' % (k.text(), alpha.text(), delta.text()))

            #CUARTA LINEA

            for011.write('%s ' % (helium_abundance.text()))

            if button_free_electrons_0.isChecked() == True:
                for011.write('0.0\n')
            if button_free_electrons_1.isChecked() == True:
                for011.write('1.0\n')
            if button_free_electrons_2.isChecked() == True:
                for011.write('2.0\n')

            #QUINTA LINEA

            if button_PPK.isChecked() == True:
                for011.write('ppk ')
            if button_CAK.isChecked() == True:
                for011.write('cak ')
            if button_FA.isChecked() == True:
                for011.write('fa ')

            if button_spline.isChecked() == True:
                for011.write('sp ')
            if button_trapezoidal.isChecked() == True:
                for011.write('tr ')

            if oblate_factor.isChecked() == True:
                for011.write('T ')
            if oblate_factor.isChecked() == False:
                for011.write('F ')

            if gravity_darkening.isChecked() == True:
                for011.write('T\n')
            if gravity_darkening.isChecked() == False:
                for011.write('F\n')

            #SEXTA LINEA

            if button_optical_depth.isChecked() == True:
                for011.write('tau ')
            if button_surface_mass.isChecked() == True:
                for011.write('den ')

            for011.write('%s\n' % (value_lower_boundary.text()))

            #SEPTIMA LINEA

            for011.write('%s %s %s\n' % (initial_zone_mesh.text(), last_zone_mesh.text(), number_mesh.text()))

            #OCTAVA LINEA

            for011.write('%s %s %s\n' % (initial_co_latitude.text(), last_co_latitude.text(), steps_co_latitude.text()))

            #NOVENA LINEA

            for011.write('%s %s\n' % (convergence_criterion.text(), factor_corrections.text()))

            #DECIMA LINEA

            if consider_v.isChecked() == True:
                for011.write('T ')
            if consider_v.isChecked() == False:
                for011.write('F ')

            if first_method.isChecked() == True:
                for011.write('T ')
            if first_method.isChecked() == False:
                for011.write('F ')

            if second_method.isChecked() == True:
                for011.write('T ')
            if second_method.isChecked() == False:
                for011.write('F ')

            if third_method.isChecked() == True:
                for011.write('T\n')
            if third_method.isChecked() == False:
                for011.write('F\n')

            #DECIMOPRIMERA LINEA

            if button_trial_velocity_acc.isChecked() == True:
                for011.write('acc ')
            if button_trial_velocity_fast.isChecked() == True:
                for011.write('fast ')
            if button_trial_velocity_blaw.isChecked() == True:
                for011.write('manual %s %s %s ' % (b_value.text(), hyperbolic_excess_speed.text(), eigenvalue.text()))
            if button_trial_velocity_blaw.isChecked() == False:
                for011.write('0.0 0.0 0.0 ')

            if try_additional_trial_velocity.isChecked() == False:
                for011.write('F')
                for011.close()

            if try_additional_trial_velocity.isChecked() == True:
                for011.write('T\n')
                for i in range(1, Window.INPUT_number_of_trials+1):
                    exec("if Window.button_trial_velocity_acc_"+str(i)+".isChecked() == True:\n\tfor011.write('acc ')\nif Window.button_trial_velocity_fast_"+str(i)+".isChecked() == True:\n\tfor011.write('fast ')\nif Window.button_trial_velocity_blaw_"+str(i)+".isChecked() == True:\n\tfor011.write('manual %s %s %s ' % (Window.b_value_"+str(i)+".text(), Window.hyperbolic_excess_speed_"+str(i)+".text(), Window.eigenvalue_"+str(i)+".text()))\nif Window.button_trial_velocity_blaw_"+str(i)+".isChecked() == False:\n\tfor011.write('0.0 0.0 0.0 ')")
                    if i!=Window.INPUT_number_of_trials:
                        for011.write('T\n')
                    if i==Window.INPUT_number_of_trials:
                        for011.write('F')
                        for011.close()
            
            #Ejecutando el script de Fortran:

            if prepend_model_name.isChecked()==True:

                call(['../hydwind'])

            #Ahora que ya estan todos los "for00X" creados, hago que se ploteen las cosas guiandome por el script de Ignacio:





            
            
            ########SCRIPT DE IGNACIO MODIFICADO:############################################################

            #Por la estructura de matplotlib, tengo que tener creado el Figure del PDF aun cuando ni siquiera le hemos preguntado al usuario si quiere guardar los graficos. Si no lo hago ahora, no podre hacerlo despues porque los Axes se crearian antes del Figure del PDF y me tiraria error

            global results_pdf_fig

            results_pdf_fig, pdf_axes = pl.subplots(4, 2)
            results_pdf_fig.set_size_inches(8.5, 11.)
            left  = 0.03  # the left side of the subplots of the figure
            right = 0.98    # the right side of the subplots of the figure
            bottom = 0.05   # the bottom of the subplots of the figure
            top = 0.97      # the top of the subplots of the figure
            wspace = 0.01   # the amount of width reserved for blank space between subplots
            hspace = 0.35   # the amount of height reserved for white space between subplot
            pl.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

            #Ahora hacemos que se definan los parametros:

            if prepend_model_name.isChecked()==True:
                prefile = model_name.text()+'-'

            if prepend_model_name.isChecked()==False:
                prefile=''
            
            # HYDWIND model
            # Parameters
            files1 = prefile+'for002.dat'
            pfile = open(files1, 'r')  # Open file for reading
            lines=pfile.readlines()          # Read ALL rows in infile
            params = [i.split() for i in lines];  # Split every line
            # Each parameter from row "job" is defined
            model = params[5][3];  yhe = float(params[20][2]);  zhe = float(params[20][5]);
            ahe = float('4.0');
            rsun = 6.96e10; msun = 1.99e33; lsun = 3.90e33;
            year = 3600*24*365.25; kbol = 1.38e-16; mh = 1.67e-24;
            mue = (1.0 + ahe*yhe)/(2.0 + yhe*(1.0 + zhe));
            rcrit = float(params[42][2]); vcrit = float(params[43][5]); dwcrit = float(params[44][2]);
            mloss = staxml = float(params[46][5]); stavinf = float(params[50][2]);
            teff = float(params[9][2]); logg = float(params[10][2]); rstar = float(params[12][4]);
            rs = rstar*rsun; ms = float(params[13][5])*msun; ls = float(params[14][5])*lsun;
            kion=float(params[30][2]); Alpha=float(params[30][5]); Delta=float(params[31][2]);
            Omega=float(params[17][5])
            ciso = math.sqrt(kbol*teff/(mh*mue))
            pfile.close();                  # Close file
            #
            files2 = prefile+'for007.dat'
            for007F = np.genfromtxt(files2)
            nn = len(for007F[:,0])
            grmax = max(for007F[:,3]);
            dvrmax = max(np.log10(for007F[:,3]*ciso/(rs*for007F[:,0]**2.0)))
            dvrmin = min(np.log10(for007F[:,3]*ciso/(rs*for007F[:,0]**2.0)))
            glinemax = max(for007F[:,8]);
            rciso = interp1d(for007F[:,2],for007F[:,0])(ciso*1e-5)
            unit = (msun*1e-6)/year

            #Ahora se hacen los QLabels con cada una de las 8 figuras del PPT:

            #1) EL RESUMEN:

            global box_parameters
            global box_results

            box_parameters = QGroupBox('Stellar Parameters used:')
            box_parameters.setFont(QFont('Arial', 12))
            box_parameters_layout = QVBoxLayout()
            box_parameters.setLayout(box_parameters_layout)

            parameters_1st_row = QLabel('<pre>T<sub>eff</sub> = '+'{0}'.format(teff)+' [K]</pre>')
            box_parameters_layout.addWidget(parameters_1st_row)

            parameters_2nd_row = QLabel('<pre>log(g) = '+'{0} '.format(logg)+'  R<sub>*</sub> = '+'{0}'.format(rstar)+'[R\u2299]</pre>')
            box_parameters_layout.addWidget(parameters_2nd_row)

            parameters_3rd_row = QLabel('<pre>\u03A9 = '+'{0}</pre>'.format(Omega))
            box_parameters_layout.addWidget(parameters_3rd_row)

            parameters_4th_row = QLabel('<pre>k = '+"{0}".format(kion)+'   \u03b1 = '+"{0}".format(Alpha) +'   \u03b4 = '+"{0}".format(Delta))
            box_parameters_layout.addWidget(parameters_4th_row)

            box_results = QGroupBox('Results:')
            box_results.setFont(QFont('Arial', 12))
            box_results_layout = QVBoxLayout()
            box_results.setLayout(box_results_layout)

            results_1st_row = QLabel('<pre>&rho;<sub>0</sub> = '+"{0}&#10005;10<sup>{1}</sup>".format(format(for007F[0,5],'.2e')[:4],format(for007F[0,5],'.2e')[5:8])+' [gr cm<sup>-3</sup>]</pre>')
            box_results_layout.addWidget(results_1st_row)

            results_2nd_row = QLabel('<pre>v<sub>0</sub> = '+ "{0}&#10005;10<sup>{1}</sup>".format(format(for007F[0,2],'.2e')[:4],format(for007F[0,2],'.2e')[5:8])+' [km s<sup>-1</sup>]</pre>')
            box_results_layout.addWidget(results_2nd_row)

            results_3rd_row = QLabel('<pre>v<sub>&infin;</sub> = '+ "{0}&#10005;10<sup>{1}</sup>".format(format(for007F[-1,2],'.2e')[:4],format(for007F[-1,2],'.2e')[5:8])+' [km s<sup>-1</sup>]</pre>')
            box_results_layout.addWidget(results_3rd_row)

            results_4th_row = QLabel('<pre>\u1e40 = '+"{0}&#10005;10<sup>{1}</sup>".format(format(staxml,'.2e')[:4],format(staxml,'.2e')[5:8])+' [10<sup>-6</sup> M\u2299 yr<sup>-1</sup>]</pre>')
            box_results_layout.addWidget(results_4th_row)
            

            #2) EL VELOCITY PROFILE:

            global velocity_profile_fig_label
            velocity_profile_fig_label = QLabel()
            
            prange= [-1.01,0.0,0.0,stavinf+50]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6
                       
            #Plot individual:
            
            velocity_profile_fig = pl.figure(figsize=(4.6, 3.65))
            velocity_profile_axes = pl.axes()
            velocity_profile_fig.add_axes(velocity_profile_axes)
            velocity_profile_axes.set_aspect(aspectrec)
            velocity_profile_axes.plot(for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND')
            velocity_profile_axes.set_title('Velocity Profile',fontsize=8, fontweight='bold')
            velocity_profile_axes.set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            velocity_profile_axes.set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=1) 
            velocity_profile_axes.tick_params(labelsize=7.5)
            velocity_profile_axes.axis(prange)
            velocity_profile_axes.legend(loc='upper left',frameon=False,fontsize=6.3,handlelength=2)
            velocity_profile_axes.grid(True,linestyle=':')
            velocity_profile_fig.savefig('disposable.png', transparent=True)
            velocity_profile_pixmap = QPixmap('disposable.png')
            velocity_profile_fig_label.setPixmap(velocity_profile_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:
            
            pdf_axes[0, 0].set_aspect(aspectrec)
            pdf_axes[0, 0].plot(for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND')
            pdf_axes[0, 0].set_title('Velocity Profile',fontsize=8, fontweight='bold')
            pdf_axes[0, 0].set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            pdf_axes[0, 0].set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=1) 
            pdf_axes[0, 0].tick_params(labelsize=7.5)
            pdf_axes[0, 0].axis(prange)
            pdf_axes[0, 0].legend(loc='upper left',frameon=False,fontsize=6.3,handlelength=2)
            pdf_axes[0, 0].grid(True,linestyle=':')


            #3) EL VELOCITY PROFILE CON TRIAL:

            global velocity_profile_trial_fig_label
            velocity_profile_trial_fig_label = QLabel()

            prange= [-1.01,0.0,0.0,stavinf+50]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            velocity_profile_trial_fig = pl.figure(figsize=(4.6, 3.65))
            velocity_profile_trial_axes = pl.axes()
            velocity_profile_trial_fig.add_axes(velocity_profile_trial_axes)
            velocity_profile_trial_axes.set_aspect(aspectrec)
            velocity_profile_trial_axes.plot(for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND');
            velocity_profile_trial_axes.plot(for007F[:,1],for007F[:,16],linestyle='-',color='r', label='TRIAL PROFILE');  
            velocity_profile_trial_axes.set_title('Velocity Profile',fontsize=8, fontweight='bold')
            velocity_profile_trial_axes.set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            velocity_profile_trial_axes.set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=1) 
            velocity_profile_trial_axes.tick_params(labelsize=7.5)
            velocity_profile_trial_axes.axis(prange)
            velocity_profile_trial_axes.legend(loc='upper left',frameon=False,fontsize=6.3,handlelength=2)
            velocity_profile_trial_axes.grid(True,linestyle=':')
            velocity_profile_trial_fig.savefig('disposable.png', transparent=True)
            velocity_profile_trial_pixmap = QPixmap('disposable.png')
            velocity_profile_trial_fig_label.setPixmap(velocity_profile_trial_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:
            
            pdf_axes[1, 0].set_aspect(aspectrec)
            pdf_axes[1, 0].plot(for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND');
            pdf_axes[1, 0].plot(for007F[:,1],for007F[:,16],linestyle='-',color='r', label='TRIAL PROFILE');  
            pdf_axes[1, 0].set_title('Velocity Profile',fontsize=8, fontweight='bold')
            pdf_axes[1, 0].set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            pdf_axes[1, 0].set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=1) 
            pdf_axes[1, 0].tick_params(labelsize=7.5)
            pdf_axes[1, 0].axis(prange)
            pdf_axes[1, 0].legend(loc='upper left',frameon=False,fontsize=6.3,handlelength=2)
            pdf_axes[1, 0].grid(True,linestyle=':')

            
            #4) V INNER:

            global v_inner_fig_label
            v_inner_fig_label = QLabel()

            prange= [0.999,rciso + 0.007,0.0,20+ciso*1e-5]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            v_inner_fig = pl.figure(figsize=(4.6, 3.65))
            v_inner_axes = pl.axes()
            v_inner_fig.add_axes(v_inner_axes)
            v_inner_axes.set_aspect(aspectrec)
            v_inner_axes.plot(-1/for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND');
            v_inner_axes.set_title('V(r/R$_{*}$) (inner)',fontsize=8, y=0.99, fontweight='bold')
            v_inner_axes.set_xlabel('r/R$_{*}$',fontsize=7.5);
            v_inner_axes.set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=-0);
            v_inner_axes.tick_params(labelsize=7.5)
            v_inner_axes.axis(prange)
            v_inner_axes.grid(True,linestyle=':')
            v_inner_fig.savefig('disposable.png', transparent=True)
            v_inner_pixmap = QPixmap('disposable.png')
            v_inner_fig_label.setPixmap(v_inner_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:

            pdf_axes[0, 1].set_aspect(aspectrec)
            pdf_axes[0, 1].plot(-1/for007F[:,1],for007F[:,2],linestyle='-',color='b', label='HYDWIND');
            pdf_axes[0, 1].set_title('V(r/R$_{*}$) (inner)',fontsize=8, y=0.99, fontweight='bold')
            pdf_axes[0, 1].set_xlabel('r/R$_{*}$',fontsize=7.5);
            pdf_axes[0, 1].set_ylabel('v  [km s$^{-1}$]',fontsize=7.5,labelpad=-0);
            pdf_axes[0, 1].tick_params(labelsize=7.5)
            pdf_axes[0, 1].axis(prange)
            pdf_axes[0, 1].grid(True,linestyle=':')


            #5) DV/DR:

            global dv_dr_fig_label
            dv_dr_fig_label = QLabel()

            prange= [-5.0,100.0,dvrmin*1.1, dvrmax*0.9]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            dv_dr_fig = pl.figure(figsize=(4.6, 3.65))
            dv_dr_axes = pl.axes()
            dv_dr_fig.add_axes(dv_dr_axes)
            dv_dr_axes.set_aspect(aspectrec)
            dv_dr_axes.plot(for007F[:,0],np.log10(for007F[:,3]*ciso*(for007F[:,0]**-2)/rs),linestyle='-',color='b', label='HYDWIND');
            dv_dr_axes.set_title('dv/dr',fontsize=8, fontweight='bold')
            dv_dr_axes.set_xlabel('r/R$_{*}$',fontsize=7.5);
            dv_dr_axes.set_ylabel('log (dv/dr)',fontsize=7.5,labelpad=-0);
            dv_dr_axes.tick_params(labelsize=7.5)
            dv_dr_axes.axis(prange)
            dv_dr_axes.grid(True,linestyle=':')
            dv_dr_fig.savefig('disposable.png', transparent=True)
            dv_dr_pixmap = QPixmap('disposable.png')
            dv_dr_fig_label.setPixmap(dv_dr_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:

            pdf_axes[1, 1].set_aspect(aspectrec)
            pdf_axes[1, 1].plot(for007F[:,0],np.log10(for007F[:,3]*ciso*(for007F[:,0]**-2)/rs),linestyle='-',color='b', label='HYDWIND');
            pdf_axes[1, 1].set_title('dv/dr',fontsize=8, fontweight='bold')
            pdf_axes[1, 1].set_xlabel('r/R$_{*}$',fontsize=7.5);
            pdf_axes[1, 1].set_ylabel('log (dv/dr)',fontsize=7.5,labelpad=-0);
            pdf_axes[1, 1].tick_params(labelsize=7.5)
            pdf_axes[1, 1].axis(prange)
            pdf_axes[1, 1].grid(True,linestyle=':')

            
            #6) DW/DU:

            global dw_du_fig_label
            dw_du_fig_label = QLabel()

            prange= [-1.01,0.0,0.0,grmax + 50.0]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            dw_du_fig = pl.figure(figsize=(4.6, 3.65))
            dw_du_axes = pl.axes()
            dw_du_fig.add_axes(dw_du_axes)
            dw_du_axes.set_aspect(aspectrec)
            dw_du_axes.plot(for007F[:,1],for007F[:,3],linestyle='-',color='b', label='HYDWIND');
            dw_du_axes.set_title('dw/du',fontsize=8, fontweight='bold');
            dw_du_axes.set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            dw_du_axes.set_ylabel('dw/du',fontsize=7.5,labelpad=-0);
            dw_du_axes.tick_params(labelsize=7.5)
            dw_du_axes.axis(prange)
            dw_du_axes.grid(True,linestyle=':')
            dw_du_fig.savefig('disposable.png', transparent=True)
            dw_du_pixmap = QPixmap('disposable.png')
            dw_du_fig_label.setPixmap(dw_du_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:
        
            pdf_axes[2, 0].set_aspect(aspectrec)
            pdf_axes[2, 0].plot(for007F[:,1],for007F[:,3],linestyle='-',color='b', label='HYDWIND');
            pdf_axes[2, 0].set_title('dw/du',fontsize=8, fontweight='bold');
            pdf_axes[2, 0].set_xlabel('u = -R$_{*}$/r',fontsize=7.5);
            pdf_axes[2, 0].set_ylabel('dw/du',fontsize=7.5,labelpad=-0);
            pdf_axes[2, 0].tick_params(labelsize=7.5)
            pdf_axes[2, 0].axis(prange)
            pdf_axes[2, 0].grid(True,linestyle=':')


            #7) DENSITY:

            global density_fig_label
            density_fig_label = QLabel()

            prange= [-4, 2.1,np.log10(min(for007F[1:,5])*0.5),np.log10(max(for007F[1:,5])*10.)]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            density_fig = pl.figure(figsize=(4.6, 3.65))
            density_axes = pl.axes()
            density_fig.add_axes(density_axes)
            density_axes.set_aspect(aspectrec)
            density_axes.plot(np.log10(for007F[1:,0]-1.0),np.log10(for007F[1:,5]),linestyle='-',color='b', label='HYDWIND');
            density_axes.set_title('Density',fontsize=8, fontweight='bold');
            density_axes.set_xlabel('log (r/R$_{*} - 1)$',fontsize=7.5);
            density_axes.set_ylabel(r'log ($\rho$)',fontsize=7.5,labelpad=-0);
            density_axes.tick_params(labelsize=7.5)
            density_axes.axis(prange)
            density_axes.grid(True,linestyle=':')
            density_fig.savefig('disposable.png', transparent=True)
            density_pixmap = QPixmap('disposable.png')
            density_fig_label.setPixmap(density_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:

            pdf_axes[2, 1].set_aspect(aspectrec)
            pdf_axes[2, 1].plot(np.log10(for007F[1:,0]-1.0),np.log10(for007F[1:,5]),linestyle='-',color='b', label='HYDWIND');
            pdf_axes[2, 1].set_title('Density',fontsize=8, fontweight='bold');
            pdf_axes[2, 1].set_xlabel('log (r/R$_{*} - 1)$',fontsize=7.5);
            pdf_axes[2, 1].set_ylabel(r'log ($\rho$)',fontsize=7.5,labelpad=-0);
            pdf_axes[2, 1].tick_params(labelsize=7.5)
            pdf_axes[2, 1].axis(prange)
            pdf_axes[2, 1].grid(True,linestyle=':')
            

            #8) G-LINE:

            global g_line_fig_label
            g_line_fig_label = QLabel()

            prange= [-5.0,100.0,-100, glinemax*1.1]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.6

            #Plot individual:

            g_line_fig = pl.figure(figsize=(4.6, 3.65))
            g_line_axes = pl.axes()
            g_line_fig.add_axes(g_line_axes)
            g_line_axes.set_aspect(aspectrec)
            g_line_axes.plot(for007F[:,0],for007F[:,8],linestyle='-',color='b', label='HYDWIND');
            g_line_axes.set_title('g_line',fontsize=8, fontweight='bold');
            g_line_axes.set_xlabel('r/R$_{*}$',fontsize=7.5);
            g_line_axes.set_ylabel('$g_{line}$',fontsize=7.5,labelpad=-0);
            g_line_axes.tick_params(labelsize=7.5)
            g_line_axes.axis(prange)
            g_line_axes.grid(True,linestyle=':')
            g_line_fig.savefig('disposable.png', transparent=True)
            g_line_pixmap = QPixmap('disposable.png')
            g_line_fig_label.setPixmap(g_line_pixmap)
            call(['rm', 'disposable.png'])

            #Plot para el PDF:

            pdf_axes[3, 0].set_aspect(aspectrec)
            pdf_axes[3, 0].plot(for007F[:,0],for007F[:,8],linestyle='-',color='b', label='HYDWIND');
            pdf_axes[3, 0].set_title('g_line',fontsize=8, fontweight='bold');
            pdf_axes[3, 0].set_xlabel('r/R$_{*}$',fontsize=7.5);
            pdf_axes[3, 0].set_ylabel('$g_{line}$',fontsize=7.5,labelpad=-0);
            pdf_axes[3, 0].tick_params(labelsize=7.5)
            pdf_axes[3, 0].axis(prange)
            pdf_axes[3, 0].grid(True,linestyle=':') 

            
            #9) RESUMEN PDF:

            parameters1 = '\n\nStellar Parameters:'
            parameters2 = '\nT$_{\mathrm{eff}}$ = '+'{0}'.format(teff)+' [K]    '+'  $\Omega$= '+'{0}'.format(Omega)
            parameters3=  '\nlog $g$= '+'{0}'.format(logg)+'  R$_{*}$= '+'{0}'.format(rstar)+' [R$_{\odot}$]'
            parameters4= '\n'r'$k$= '+"${0}$  ".format(kion)+r'$\alpha$= '+"${0}$  ".format(Alpha) +r'$\delta$= '+"${0}$".format(Delta)  
            parameters5 = '\nResults:\n'r'$\rho_{0}$= '+"${0} \\times 10^{{{1}}}$".format(format(for007F[0,5],'.2e')[:4],format(for007F[0,5],'.2e')[5:8])+' [gr cm$^{-3}$]'
            parameters6=  '\nv$_{0}$='+ "${0} \\times 10^{{{1}}}$".format(format(for007F[0,2],'.2e')[:4],format(for007F[0,2],'.2e')[5:8])+' [km s$^{-1}$]'+'\n'+'v$_{\infty}$='+ "${0} \\times 10^{{{1}}}$".format(format(for007F[-1,2],'.2e')[:4],format(for007F[-1,2],'.2e')[5:8])+' [km s$^{-1}$]'
            parameters7= '\n$\dot{M}$= '+"${0} \\times 10^{{{1}}}$".format(format(staxml,'.2e')[:4],format(staxml,'.2e')[5:8])+' [$10^{-6}$ M$_{\odot}$ yr$^{-1}$]'
            tt='Model: '+model+parameters1+parameters2+parameters3+parameters4+parameters5+parameters6+parameters7
            left, width = .01, .98
            bottom, height = .01, .98
            right = left + width
            top = bottom + height
            prange= [left, right,bottom,top]
            aspectrec=(prange[1]-prange[0])/(prange[3]-prange[2])*0.8
            pdf_axes[3, 1].set_aspect(aspectrec)
            p = patches.Rectangle((left, bottom), width, height,fill=False, clip_on=False, lw=2)
            pdf_axes[3, 1].add_patch(p)
            pdf_axes[3, 1].patch.set_visible(False)
            pdf_axes[3, 1].axis('off')
            pdf_axes[3, 1].text(0.02*(left+right), 0.5*(bottom+top), tt,horizontalalignment='left', verticalalignment='center',fontsize=10, color='black')
            pdf_axes[3, 1].text(0.8*(left+right), -0.15*(bottom+top), '$\copyright$ Hydwind',horizontalalignment='left', verticalalignment='bottom',fontsize=10, color='black')


            ######AQUI TERMINAN DE TRABAJARSE LOS PLOTS#######

            global Hydwind_Results
            Hydwind_Results = Results()



        button_run.clicked.connect(run_app)
            
            

        self.show()
    
#Creando ventana de Resultados:

class Results(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(470) #525
        self.setFixedWidth(900) #860
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QHBoxLayout()
        skeleton.setLayout(skeleton_layout)

        all_columns = QGroupBox('                                                                               MODEL: '+model_name.text())
        all_columns_layout = QHBoxLayout()
        all_columns.setLayout(all_columns_layout)
        skeleton_layout.addWidget(all_columns)

        #PARTE IZQUIERDA

        left_column = QWidget()
        left_column_layout = QVBoxLayout()
        left_column.setLayout(left_column_layout)
        all_columns_layout.addWidget(left_column)

        left_column_layout.addWidget(box_parameters)
        left_column_layout.addWidget(box_results)

        #Botones de guardado

        saving_buttons = QWidget()
        saving_buttons_layout = QGridLayout()
        saving_buttons.setLayout(saving_buttons_layout)
        left_column_layout.addWidget(saving_buttons)

        button_back_save = QPushButton('Save PDF and return', minimumWidth=170, minimumHeight=40)
        saving_buttons_layout.addWidget(button_back_save, 0, 0, alignment=Qt.AlignCenter)
        button_back_no_save = QPushButton("Don't save PDF and return", minimumWidth=170, minimumHeight=40)
        saving_buttons_layout.addWidget(button_back_no_save, 1, 0, alignment=Qt.AlignCenter)
        button_exit_save = QPushButton("Save PDF and exit", minimumWidth=170, minimumHeight=40)
        saving_buttons_layout.addWidget(button_exit_save, 0, 1, alignment=Qt.AlignCenter)
        button_exit_no_save = QPushButton("Don't save PDF and exit", minimumWidth=170, minimumHeight=40)
        saving_buttons_layout.addWidget(button_exit_no_save, 1, 1, alignment=Qt.AlignCenter)

        #Funciones de esos botones: (sus Prompts se definiran al final)
    
        #Guardar y atras:

        def back_save():
            results_pdf_fig.savefig(model_name.text()+'.pdf')
            chdir(original_path)
            self.hide()
            global Hydwind_Back_Saved_Prompt
            Hydwind_Back_Saved_Prompt = Back_Saved_Prompt() #1ER PROMPT
        
        button_back_save.clicked.connect(back_save)

        #No guardar y atras:

        def back_no_save():
            chdir(original_path)
            self.hide()

        button_back_no_save.clicked.connect(back_no_save)

        #Guardar y salir:

        def exit_save():
            results_pdf_fig.savefig(model_name.text()+'.pdf')
            global Hydwind_Exit_Saved_Prompt
            Hydwind_Exit_Saved_Prompt = Exit_Saved_Prompt() #2DO PROMPT
            Hydwind_Window.close()
            Hydwind_Results.close()

        button_exit_save.clicked.connect(exit_save)

        #No guardar y salir:

        def exit_no_save():
            global Hydwind_Exit_Not_Saved_Prompt
            Hydwind_Exit_Not_Saved_Prompt = Exit_Not_Saved_Prompt() #3ER PROMPT
            
        button_exit_no_save.clicked.connect(exit_no_save)


        #PARTE DERECHA

        right_column = QWidget()
        right_column_layout = QVBoxLayout()
        right_column.setLayout(right_column_layout)
        all_columns_layout.addWidget(right_column)

        plot_box = QGroupBox('Plots:')
        plot_box.setFont(QFont('Arial', 12))
        plot_box_layout = QVBoxLayout()
        plot_box.setLayout(plot_box_layout)
        right_column_layout.addWidget(plot_box)
        
        #Plots:

        plot_box_layout.addWidget(velocity_profile_fig_label)
        velocity_profile_trial_fig_label.hide()
        plot_box_layout.addWidget(velocity_profile_trial_fig_label)
        v_inner_fig_label.hide()
        plot_box_layout.addWidget(v_inner_fig_label)
        dv_dr_fig_label.hide()
        plot_box_layout.addWidget(dv_dr_fig_label)
        dw_du_fig_label.hide()
        plot_box_layout.addWidget(dw_du_fig_label)
        density_fig_label.hide()
        plot_box_layout.addWidget(density_fig_label)
        g_line_fig_label.hide()
        plot_box_layout.addWidget(g_line_fig_label)


        plot_buttons = QWidget()
        plot_buttons_layout = QGridLayout()
        plot_buttons.setLayout(plot_buttons_layout)
        plot_box_layout.addWidget(plot_buttons)

        show_trial_plot = QCheckBox('Show Trial Velocity Profile plot on graph')
        show_trial_plot.setFont(QFont('Arial', 9))
        plot_buttons_layout.addWidget(show_trial_plot, 0, 0, alignment=Qt.AlignLeft)        

        def toggle_trial_velocity_plot():
            if show_trial_plot.isChecked()==True:
                velocity_profile_fig_label.hide()
                velocity_profile_trial_fig_label.show()
            if show_trial_plot.isChecked()==False:
                velocity_profile_trial_fig_label.hide()
                velocity_profile_fig_label.show()

        show_trial_plot.toggled.connect(toggle_trial_velocity_plot)

        previous_plot_button = QPushButton('\u25C0', maximumWidth=30)
        next_plot_button = QPushButton("\u25B6", maximumWidth=30)
        plot_buttons_layout.addWidget(previous_plot_button, 0, 1)
        plot_buttons_layout.addWidget(next_plot_button, 0, 2)
        
        #Dandole funcionalidad a los botones de adelante y atras de los plots

        previous_plot_button.setDisabled(True)

        def next_plot(plot_counter):

            if velocity_profile_fig_label.isVisible() == True or velocity_profile_trial_fig_label.isVisible() == True:
                show_trial_plot.setChecked(False)
                show_trial_plot.setDisabled(True)
                velocity_profile_fig_label.hide()
                v_inner_fig_label.show()
                previous_plot_button.setDisabled(False)
                return 0

            if v_inner_fig_label.isVisible() == True:
                v_inner_fig_label.hide()
                dv_dr_fig_label.show()
                return 0

            if dv_dr_fig_label.isVisible() == True:
                dv_dr_fig_label.hide()
                dw_du_fig_label.show()
                return 0

            if dw_du_fig_label.isVisible() == True:
                dw_du_fig_label.hide()
                density_fig_label.show()
                return 0

            if density_fig_label.isVisible() == True:
                density_fig_label.hide()
                g_line_fig_label.show()
                next_plot_button.setDisabled(True)
                return 0

        next_plot_button.clicked.connect(next_plot)

        def previous_plot():
            
            if g_line_fig_label.isVisible() == True:
                g_line_fig_label.hide()
                density_fig_label.show()
                next_plot_button.setDisabled(False)
                return 0

            if density_fig_label.isVisible() == True:
                density_fig_label.hide()
                dw_du_fig_label.show()
                return 0

            if dw_du_fig_label.isVisible() == True:
                dw_du_fig_label.hide()
                dv_dr_fig_label.show()
                return 0
                
            if dv_dr_fig_label.isVisible() == True:
                dv_dr_fig_label.hide()
                v_inner_fig_label.show()
                return 0

            if v_inner_fig_label.isVisible() == True:
                v_inner_fig_label.hide()
                velocity_profile_fig_label.show()
                show_trial_plot.setDisabled(False)
                previous_plot_button.setDisabled(True)
                return 0

        previous_plot_button.clicked.connect(previous_plot)

        self.show()

#Definiendo los Prompts de los botones de guardado:

#PRIMER PROMPT:

class Back_Saved_Prompt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(120)
        self.setFixedWidth(250)
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)
        text = QLabel('<b>PDF saved succesfully.</b>')
        button = QPushButton('Continue')
        skeleton_layout.addWidget(text, alignment=Qt.AlignCenter)
        skeleton_layout.addWidget(button, alignment=Qt.AlignCenter)
        button.clicked.connect(self.hide)
        self.show()


#SEGUNDO PROMPT:

class Exit_Saved_Prompt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(110)
        self.setFixedWidth(400)
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)
        text = QLabel('<b>PDF saved succesfully.</b>')
        text2 = QLabel('Thank you for using Hydwind GUI v1.1.4')
        text3 = QLabel('<i>by Alonso Guerrero C. (alonso.guerrero@alumnos.uv.cl)</i>')
        skeleton_layout.addWidget(text, alignment=Qt.AlignCenter)
        skeleton_layout.addWidget(text2, alignment=Qt.AlignCenter)
        skeleton_layout.addWidget(text3, alignment=Qt.AlignCenter)
        button = QPushButton('Close')
        skeleton_layout.addWidget(button, alignment=Qt.AlignCenter)
        button.clicked.connect(self.close)
        self.show()

#TERCER PROMPT:

class Exit_Not_Saved_Prompt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(110)
        self.setFixedWidth(400)
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)
        text = QLabel('<b>Confirm exiting without saving:</b>')
        skeleton_layout.addWidget(text, alignment=Qt.AlignCenter)
        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        buttons.setLayout(buttons_layout)
        skeleton_layout.addWidget(buttons, alignment=Qt.AlignCenter)
        no = QPushButton('Go back')
        yes = QPushButton('Confirm')
        buttons_layout.addWidget(no)
        no.clicked.connect(self.close)
        buttons_layout.addWidget(yes)
        
        def confirm_exiting():
            Hydwind_Window.close()
            Hydwind_Results.close()
            global Hydwind_Final_Prompt
            Hydwind_Final_Prompt = Final_Prompt() #4TO PROMPT
            self.close()

        yes.clicked.connect(confirm_exiting)
        
        self.show()

#CUARTO PROMPT:

class Final_Prompt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hydwind GUI v1.1.4')
        self.setFixedHeight(110)
        self.setFixedWidth(400)
        skeleton = QWidget()
        self.setCentralWidget(skeleton)
        skeleton_layout = QVBoxLayout()
        skeleton.setLayout(skeleton_layout)
        text = QLabel('<b>Thank you for using Hydwind GUI v1.1.4</b>')
        text2 = QLabel('<i>by Alonso Guerrero C. (alonso.guerrero@alumnos.uv.cl)</i>')
        skeleton_layout.addWidget(text, alignment=Qt.AlignCenter)
        skeleton_layout.addWidget(text2, alignment=Qt.AlignCenter)
        button = QPushButton('Close')
        skeleton_layout.addWidget(button, alignment=Qt.AlignCenter)
        button.clicked.connect(self.close)
        self.show()


#Ejecutando toda la APP:

Hydwind_GUI = QApplication([])
Hydwind_Prompt = Prompt()

Hydwind_GUI.exec()







































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































