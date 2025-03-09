import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        df = pd.read_csv(self.file_path)
        qgl = df['qgl'].tolist()
        q_fluid_wells = df.iloc[: , 1:].T.to_numpy().tolist()
        return qgl, q_fluid_wells


if __name__ == "__main__":
    load = DataLoader('./data/datos.csv')
    qgl, fluids = load.load_data()
    print(fluids)