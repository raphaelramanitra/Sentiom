import sqlite3
import os

db_path = "./sentiom.db"
print(f"Chemin absolu testé : {os.path.abspath(db_path)}")
print(f"Le fichier existe ? {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # On interroge telemetry_data et non telemetry
        cursor.execute("SELECT COUNT(*) FROM telemetry_data")
        count = cursor.fetchone()[0]
        print(f"Nombre de lignes dans la table telemetry_data : {count}")
        
        cursor.execute("SELECT * FROM telemetry_data")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Erreur : {e}")
    conn.close()