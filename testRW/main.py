import fastf1 as f1
# from src import timesfm
import numpy as np
from fastf1.livetiming.client import SignalRClient

f1.Cache.enable_cache('../cache/')

live_sesh = SignalRClient('./live_data.txt', filemode='w', debug=False, timeout=60, logger=None)
print('starting log')
live_sesh.start()
# session = f1.get_session(2024, 1, 'R')
# session.load()
# lap_data = session.laps.pick_driver('VER')

# print(lap_data)

# tfm = timesfm.TimesFm(
#     context_len=32,
#     horizon_len=32,
#     input_patch_len=32,
#     output_patch_len=128,
#     num_layers=20,
#     model_dims=1280,
#     backend='cpu',
# )
# tfm.load_from_checkpoint(repo_id="google/timesfm-1.0-200m")

# forecast_input = [
#     np.sin(np.linspace(0, 20, 100)),
#     np.sin(np.linspace(0, 20, 200)),
#     np.sin(np.linspace(0, 20, 400)),
# ]
# frequency_input = [0, 1, 2]

# point_forecast, experimental_quantile_forecast = tfm.forecast(
#     forecast_input,
#     freq=frequency_input,
# )

