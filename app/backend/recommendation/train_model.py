import os
import pickle

def _initialize_engine(self):
    matrix_path = 'backend/recommendation/models/similarity_matrix.pkl'
    df_path = 'backend/recommendation/models/processed_df.pkl'

    if os.path.exists(matrix_path) and os.path.exists(df_path):
        print("⚡ Loading pre-computed ML models from disk...")
        with open(matrix_path, 'rb') as f:
            self.cosine_sim = pickle.load(f)
        self.df = pd.read_pickle(df_path)
        self.indices = pd.Series(self.df.index, index=self.df['id']).drop_duplicates()
    else:
        print("⚠️  Pre-computed models not found. Initializing full training...")
        # ... keep your existing _initialize_engine logic here as a fallback ...