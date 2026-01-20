import os
import sys
import csv
import random
import argparse
from psychopy import visual, core, event
from datetime import datetime
import numpy as np
from Paradigme_parent import Parente


class StressParadigm(Parente):
    def __init__(self, args):
        self.args = args
        self.win = None
        self.clock = core.Clock()
        
        # Paramètres du paradigme
        self.block_duration = 40  # durée par bloc
        self.pause_durations = [12.2, 14.6, 15.8, 13.4, 14.6, 14.6]  # en secondes
        self.instruction_duration = 5  # durée affichage instruction
        self.feedback_duration = 3  # secondes après réponse
        
        # Compteurs de performance
        self.correct_rotation = 0
        self.wrong_rotation = 0
        self.correct_arithmetic = 0
        self.wrong_arithmetic = 0
        
        # Paramètres arithmétiques
        self.arithmetic_start_control = 3060
        self.arithmetic_start_stress = 3073
        self.arithmetic_step = 13
        
        # Time limit pour stress runs
        self.time_limit_base = 5.0  # secondes de base
        
        # Chargement des figures de rotation mentale
        self.rotation_figures = self.load_rotation_figures()
        
    def load_rotation_figures(self):
        """Charge ou génère les stimuli de rotation mentale"""
        # Placeholder - à remplacer par de vraies figures
        # Dans une vraie implémentation, charger depuis un fichier
        figures = []
        for i in range(50):  # 50 trials possibles
            figures.append({
                'target': f'figure_{i}',
                'options': [f'option_{i}_0', f'option_{i}_1', f'option_{i}_2'],
                'correct': random.randint(0, 2)
            })
        return figures
    
    def create_window(self):
        """Crée la fenêtre d'affichage"""
        self.win = visual.Window(
            [int(self.args.largeur), int(self.args.hauteur)],
            fullscr=True,
            units='norm',
            color='black'
        )
        
    def show_instructions(self, task_type, run_type):
        """Affiche les instructions pour rotation ou arithmétique"""
        if task_type == 'rotation':
            if run_type == 'control':
                text = ("ROTATION MENTALE\n\n"
                       "Identifiez quelle figure correspond à la figure cible.\n"
                       "Utilisez les boutons 1, 2, 3 pour répondre.\n\n"
                       "Prenez votre temps, il n'y a pas de limite.")
            else:  # stress
                text = ("ROTATION MENTALE\n\n"
                       "Identifiez quelle figure correspond à la figure cible ROTÉE.\n"
                       "Répondez RAPIDEMENT avec les boutons 1, 2, 3.\n\n"
                       "ATTENTION: Temps limité!\n"
                       "Votre performance est évaluée.")
        else:  # arithmetic
            if run_type == 'control':
                text = ("CALCUL ARITHMÉTIQUE\n\n"
                       f"Nombre de départ: {self.arithmetic_start_control}\n"
                       "Soustrayez 13 à chaque fois.\n"
                       "Choisissez la bonne réponse (boutons 1-4).\n\n"
                       "Si correct: -13, si erreur: retour au début.")
            else:  # stress
                text = ("CALCUL ARITHMÉTIQUE\n\n"
                       f"Nombre de départ: {self.arithmetic_start_stress}\n"
                       "Soustrayez 13 à chaque fois.\n"
                       "Répondez RAPIDEMENT (boutons 1-4).\n\n"
                       "ATTENTION: Temps limité!\n"
                       "Si erreur: même nombre, réponses mélangées.")
        
        instruction = visual.TextStim(
            self.win,
            text=text,
            color='white',
            height=0.08,
            wrapWidth=1.6
        )
        instruction.draw()
        self.win.flip()
        core.wait(self.instruction_duration)
    
    def rotation_trial(self, run_type, trial_data):
        """Exécute un trial de rotation mentale"""
        # Affichage de la figure cible et des options
        # Placeholder - remplacer par de vraies figures visuelles
        
        target_text = visual.TextStim(
            self.win,
            text="Figure cible",
            pos=(0, 0.5),
            color='white',
            height=0.06
        )
        
        # Options de réponse
        options_text = []
        positions = [(-0.4, -0.3), (0, -0.3), (0.4, -0.3)]
        for i, pos in enumerate(positions):
            opt = visual.TextStim(
                self.win,
                text=f"Option {i+1}",
                pos=pos,
                color='white',
                height=0.06
            )
            options_text.append(opt)
        
        # Timer pour stress condition
        if run_type == 'stress':
            time_limit = self.calculate_time_limit()
            timer_text = visual.TextStim(
                self.win,
                text="",
                pos=(0, 0.8),
                color='red',
                height=0.08
            )
        
        target_text.draw()
        for opt in options_text:
            opt.draw()
        self.win.flip()
        
        onset = self.clock.getTime()
        response = None
        rt = None
        
        if run_type == 'control':
            # Pas de limite de temps
            keys = event.waitKeys(keyList=['1', '2', '3', 'escape'])
            if 'escape' in keys:
                self.win.close()
                core.quit()
            response = int(keys[0])
            rt = self.clock.getTime() - onset
        else:  # stress
            # Avec limite de temps
            start_time = core.getTime()
            while core.getTime() - start_time < time_limit:
                remaining = time_limit - (core.getTime() - start_time)
                timer_text.text = f"{remaining:.1f}s"
                
                target_text.draw()
                for opt in options_text:
                    opt.draw()
                timer_text.draw()
                self.win.flip()
                
                keys = event.getKeys(keyList=['1', '2', '3', 'escape'])
                if keys:
                    if 'escape' in keys:
                        self.win.close()
                        core.quit()
                    response = int(keys[0])
                    rt = core.getTime() - start_time
                    break
        
        # Vérifier la réponse
        correct_answer = trial_data['correct'] + 1  # +1 car les touches sont 1-3
        is_correct = (response == correct_answer) if response else False
        
        if is_correct:
            self.correct_rotation += 1
        else:
            self.wrong_rotation += 1
        
        # Feedback pour stress condition
        if run_type == 'stress' and response:
            self.show_stress_feedback(is_correct, rt, time_limit)
        
        # Afficher réponse sélectionnée pendant 3 secondes (control) ou attendre expérimentateur (stress)
        if response:
            selected = visual.TextStim(
                self.win,
                text=f"Réponse sélectionnée: {response}",
                pos=(0, 0),
                color='yellow',
                height=0.1
            )
            selected.draw()
            self.win.flip()
            
            if run_type == 'control':
                core.wait(self.feedback_duration)
            else:
                # Attendre que l'expérimentateur appuie sur une touche
                event.waitKeys(keyList=['space'])
        
        return {
            'trial_type': 'rotation',
            'run_type': run_type,
            'response': response,
            'correct': is_correct,
            'rt': rt,
            'onset': onset
        }
    
    def arithmetic_trial(self, run_type, current_number, trial_number):
        """Exécute un trial arithmétique"""
        # Calculer la bonne réponse
        correct_answer = current_number - self.arithmetic_step
        
        # Générer les distracteurs
        distractors = []
        while len(distractors) < 3:
            offset = random.randint(1, 10) * random.choice([-1, 1])
            distractor = correct_answer + offset
            if distractor not in distractors and distractor != correct_answer:
                distractors.append(distractor)
        
        # Mélanger les options
        options = [correct_answer] + distractors
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        
        # Affichage
        question_text = visual.TextStim(
            self.win,
            text=f"{current_number} - 13 = ?",
            pos=(0, 0.5),
            color='white',
            height=0.1
        )
        
        options_text = []
        positions = [(-0.5, -0.2), (-0.17, -0.2), (0.17, -0.2), (0.5, -0.2)]
        for i, (opt, pos) in enumerate(zip(options, positions)):
            opt_text = visual.TextStim(
                self.win,
                text=f"{i+1}: {opt}",
                pos=pos,
                color='white',
                height=0.08
            )
            options_text.append(opt_text)
        
        if run_type == 'stress':
            time_limit = self.calculate_time_limit()
            timer_text = visual.TextStim(
                self.win,
                text="",
                pos=(0, 0.8),
                color='red',
                height=0.08
            )
        
        question_text.draw()
        for opt in options_text:
            opt.draw()
        self.win.flip()
        
        onset = self.clock.getTime()
        response = None
        rt = None
        
        if run_type == 'control':
            keys = event.waitKeys(keyList=['1', '2', '3', '4', 'escape'])
            if 'escape' in keys:
                self.win.close()
                core.quit()
            response = int(keys[0]) - 1  # Convertir en index 0-3
            rt = self.clock.getTime() - onset
        else:  # stress
            start_time = core.getTime()
            while core.getTime() - start_time < time_limit:
                remaining = time_limit - (core.getTime() - start_time)
                timer_text.text = f"{remaining:.1f}s"
                
                question_text.draw()
                for opt in options_text:
                    opt.draw()
                timer_text.draw()
                self.win.flip()
                
                keys = event.getKeys(keyList=['1', '2', '3', '4', 'escape'])
                if keys:
                    if 'escape' in keys:
                        self.win.close()
                        core.quit()
                    response = int(keys[0]) - 1
                    rt = core.getTime() - start_time
                    break
        
        is_correct = (response == correct_index) if response is not None else False
        
        if is_correct:
            self.correct_arithmetic += 1
            next_number = correct_answer
        else:
            self.wrong_arithmetic += 1
            if run_type == 'control':
                next_number = self.arithmetic_start_control
            else:
                next_number = current_number  # Même nombre en stress
        
        # Feedback pour stress condition
        if run_type == 'stress' and response is not None:
            self.show_stress_feedback(is_correct, rt, time_limit)
        
        # Afficher réponse sélectionnée
        if response is not None:
            selected = visual.TextStim(
                self.win,
                text=f"Réponse: {options[response]}",
                pos=(0, 0),
                color='yellow',
                height=0.1
            )
            selected.draw()
            self.win.flip()
            
            if run_type == 'control':
                core.wait(self.feedback_duration)
            else:
                event.waitKeys(keyList=['space'])
        
        return {
            'trial_type': 'arithmetic',
            'run_type': run_type,
            'current_number': current_number,
            'correct_answer': correct_answer,
            'response': options[response] if response is not None else None,
            'correct': is_correct,
            'rt': rt,
            'onset': onset,
            'next_number': next_number
        }
    
    def calculate_time_limit(self):
        """Calcule le temps limite basé sur la performance"""
        total_trials = self.correct_rotation + self.wrong_rotation + self.correct_arithmetic + self.wrong_arithmetic
        if total_trials == 0:
            return self.time_limit_base
        
        accuracy = (self.correct_rotation + self.correct_arithmetic) / total_trials
        
        # Ajuster le temps: plus de précision = moins de temps
        if accuracy > 0.8:
            return max(3.0, self.time_limit_base - 1.0)
        elif accuracy < 0.5:
            return min(7.0, self.time_limit_base + 1.0)
        else:
            return self.time_limit_base
    
    def show_stress_feedback(self, is_correct, rt, time_limit):
        """Affiche feedback de stress (Erreur! ou Travaillez plus vite!)"""
        # L'expérimentateur peut choisir quel feedback afficher
        feedback_text = visual.TextStim(
            self.win,
            text="Appuyez sur 'e' pour ERREUR ou 'v' pour VITE",
            pos=(0, -0.7),
            color='gray',
            height=0.05
        )
        feedback_text.draw()
        self.win.flip()
        
        keys = event.waitKeys(keyList=['e', 'v', 'space'])
        
        if 'e' in keys:
            message = "Erreur !"
            color = 'red'
        elif 'v' in keys:
            message = "Travaillez plus vite !"
            color = 'orange'
        else:
            return  # Pas de feedback
        
        feedback = visual.TextStim(
            self.win,
            text=message,
            pos=(0, 0),
            color=color,
            height=0.15,
            bold=True
        )
        feedback.draw()
        self.win.flip()
        core.wait(1.5)
    
    def run_block(self, task_type, run_type):
        """Exécute un bloc de 40 secondes"""
        block_start = core.getTime()
        trial_count = 0
        results = []
        
        if task_type == 'arithmetic':
            if run_type == 'control':
                current_number = self.arithmetic_start_control
            else:
                current_number = self.arithmetic_start_stress
        
        while core.getTime() - block_start < self.block_duration:
            if task_type == 'rotation':
                trial_idx = trial_count % len(self.rotation_figures)
                result = self.rotation_trial(run_type, self.rotation_figures[trial_idx])
            else:  # arithmetic
                result = self.arithmetic_trial(run_type, current_number, trial_count)
                current_number = result['next_number']
            
            results.append(result)
            trial_count += 1
        
        return results
    
    def show_pause(self, duration):
        """Affiche une pause avec countdown"""
        pause_text = visual.TextStim(
            self.win,
            text="",
            pos=(0, 0),
            color='white',
            height=0.15
        )
        
        start_time = core.getTime()
        while core.getTime() - start_time < duration:
            remaining = duration - (core.getTime() - start_time)
            pause_text.text = f"Pause\n\n{remaining:.1f}s"
            pause_text.draw()
            self.win.flip()
    
    def run_paradigm(self, run_type):
        """Exécute le paradigme complet (control ou stress)"""
        all_results = []
        
        # Écran d'attente du trigger
        waiting_text = visual.TextStim(
            self.win,
            text="En attente du déclencheur 's'...",
            color='white',
            height=0.1
        )
        waiting_text.draw()
        self.win.flip()
        self.wait_for_trigger(self.args.trigger)
        
        # Séquence: 3 rotations et 3 arithmétiques alternées
        tasks = ['rotation', 'arithmetic'] * 3
        
        for i, task in enumerate(tasks):
            # Instructions
            self.show_instructions(task, run_type)
            
            # Bloc de tâche
            block_results = self.run_block(task, run_type)
            all_results.extend(block_results)
            
            # Pause (sauf après le dernier bloc)
            if i < len(tasks) - 1:
                self.show_pause(self.pause_durations[i])
        
        return all_results
    
    def save_results(self, results, run_type):
        """Sauvegarde les résultats"""
        columns = [
            'trial_type', 'run_type', 'trial_number', 'onset', 'duration',
            'response', 'correct', 'rt', 'current_number', 'correct_answer'
        ]
        
        filename, filename_csv, filename_txt = self.preprocessing_tsv_csv(
            self.args.output_file,
            {
                'Paradigm': 'Stress Protocol',
                'Run Type': run_type,
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Patient': self.args.patient_name if hasattr(self.args, 'patient_name') else 'Unknown'
            },
            paradigm_name='Stress_Protocol'
        )
        
        self.file_init(filename, filename_csv, columns)
        
        for i, result in enumerate(results):
            row = [
                result.get('trial_type', ''),
                result.get('run_type', ''),
                i + 1,
                self.float_to_csv(result.get('onset', 0)),
                '',  # Duration calculée après
                result.get('response', ''),
                1 if result.get('correct', False) else 0,
                self.float_to_csv(result.get('rt', 0)) if result.get('rt') else '',
                result.get('current_number', ''),
                result.get('correct_answer', '')
            ]
            self.write_tsv_csv(filename, filename_csv, row)
        
        # Ajouter les durées
        self.adding_duration(filename, filename_csv)
    
    def run(self):
        """Point d'entrée principal"""
        try:
            self.create_window()
            
            # Charger les instructions de lancement si fournies
            if self.args.launching:
                dossier = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
                texts = self.inputs_texts(os.path.join(dossier, self.args.launching))
                self.launching_texts(self.win, texts, self.args.trigger)
            
            # Déterminer le type de run
            run_type = self.args.run_type  # 'control' ou 'stress'
            
            # Exécuter le paradigme
            results = self.run_paradigm(run_type)
            
            # Sauvegarder
            self.save_results(results, run_type)
            
            # Message de fin
            self.the_end(self.win)
            
            # Envoyer trigger de fin si activé
            if self.args.activation:
                self.send_character(self.args.port, int(self.args.baudrate))
            
        finally:
            if self.win:
                self.win.close()
            core.quit()


def main():
    parser = argparse.ArgumentParser(description='Stress Paradigm - Control and Stress Runs')
    parser.add_argument('--run_type', type=str, required=True, choices=['control', 'stress'],
                       help='Type of run: control or stress')
    parser.add_argument('--output_file', type=str, required=True,
                       help='Output filename')
    parser.add_argument('--launching', type=str, default='',
                       help='Launching text file')
    parser.add_argument('--trigger', type=str, default='s',
                       help='Trigger key')
    parser.add_argument('--hauteur', type=str, default='1080',
                       help='Window height')
    parser.add_argument('--largeur', type=str, default='1920',
                       help='Window width')
    parser.add_argument('--port', type=str, default='COM3',
                       help='Serial port')
    parser.add_argument('--baudrate', type=str, default='9600',
                       help='Serial baudrate')
    parser.add_argument('--activation', type=bool, default=False,
                       help='Activate serial trigger')
    parser.add_argument('--patient_name', type=str, default='',
                       help='Patient name')
    
    args = parser.parse_args()
    
    paradigm = StressParadigm(args)
    paradigm.run()


if __name__ == '__main__':
    main()