# logic-main/train.py

import lightgbm as lgb
from src.config import FEATURES, TARGET
from model import get_lgbm_params, save_model
from src.features import add_interaction_features
from src.config import CAT_COLS
from src.preprocessing import cast_categorical

def train_model(train_df, valid_df, model_path):

    train_df = add_interaction_features(train_df)
    valid_df = add_interaction_features(valid_df)

    train_df = cast_categorical(train_df)
    valid_df = cast_categorical(valid_df)

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_valid = valid_df[FEATURES]
    y_valid = valid_df[TARGET]

    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    params = get_lgbm_params(scale_pos_weight)

    lgb_train = lgb.Dataset(X_train, y_train, categorical_feature=CAT_COLS)
    lgb_valid = lgb.Dataset(X_valid, y_valid, categorical_feature=CAT_COLS)

    model = lgb.train(
        params,
        lgb_train,
        valid_sets=[lgb_valid],
        num_boost_round=5000,
        callbacks=[
            lgb.early_stopping(stopping_rounds=200),
            lgb.log_evaluation(period=100)
        ]
    )

    save_model(model, model_path)
    return model
