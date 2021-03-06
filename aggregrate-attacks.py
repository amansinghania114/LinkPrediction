
import os
import csv
attack_directory = '/home/rohittulu/Semester3/LinkPrediction/travian_data/Attacks-Network-CSV'

def get_files(directory):
    return os.listdir(attack_directory)

def read_files(directory):
    files = get_files(directory)
    day_csv = {}
    for idx, fname in enumerate(files):
        fpath = os.path.join(attack_directory, fname)
        csvfile = open(fpath, 'r')
        day_csv.update({
                idx: csv.reader(csvfile, delimiter=",")
        })
    return day_csv

def get_player_ids(day_csv):
    players = set()
    for day, reader in day_csv.iteritems():
        print("Reading file: ", str(day))
        for row in reader:
            try:
                ts, play1, play2 = row
            except Exception as e:
                print(e)
            players.update([play1,play2])
    return players

def get_attack_summary_per_day(day_csv_reader):
    attacker_dict = {}
    for ts, play1, play2 in day_csv_reader:
        attacker_dict.setdefault(play1, set([])).add(play2)
    return attacker_dict

def get_attack_summary(day_to_csv_dict):
    day_to_attack_summary = {}
    for day, reader in day_to_csv_dict.iteritems():
        try:
            day_to_attack_summary.update({
                day: get_attack_summary_per_day(reader)
            })
        except Exception as e:
            print(e)
    return day_to_attack_summary

def get_aggregrate_attack_info(day_to_attack_summary):
    aggregrate_summary = {}
    for day, attack_summary in day_to_attack_summary.iteritems():
        for player1, targets in attack_summary.iteritems():
            aggregrate_summary.setdefault(player1, set()).update(targets)
    return aggregrate_summary

day_csv = read_files(attack_directory)
attack_summary = get_attack_summary(day_csv)
aggregrate_summary = get_aggregrate_attack_info(attack_summary)

save_file = "attack_summary.csv"
with open(save_file, "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    for player, targets in aggregrate_summary.iteritems():
        print "here"
        writer.writerow([player] + list(targets))
