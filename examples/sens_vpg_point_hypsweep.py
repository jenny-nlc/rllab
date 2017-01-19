#from rllab.algos.vpg import VPG
from sandbox.rocky.tf.algos.sensitive_vpg import SensitiveVPG
from rllab.baselines.linear_feature_baseline import LinearFeatureBaseline
from rllab.baselines.zero_baseline import ZeroBaseline
from examples.point_env import PointEnv
from examples.point_env_randgoal import PointEnvRandGoal
from rllab.envs.normalized_env import normalize
from rllab.misc.instrument import stub, run_experiment_lite
#from rllab.policies.gaussian_mlp_policy import GaussianMLPPolicy
from sandbox.rocky.tf.policies.sens_minimal_gauss_mlp_policy import SensitiveGaussianMLPPolicy
from sandbox.rocky.tf.envs.base import TfEnv

import tensorflow as tf

learning_rates = [1e-4, 1e-3, 1e-2]
fast_learning_rates = [0.2, 1.0, 5.0]
baselines = ['zero'] # does the same as linear

for fast_learning_rate in fast_learning_rates:
    for learning_rate in learning_rates:
        for bas in baselines:
            stub(globals())

            #env = TfEnv(normalize(PointEnv()))
            env = TfEnv(normalize(PointEnvRandGoal()))
            policy = SensitiveGaussianMLPPolicy(
                name="policy",
                env_spec=env.spec,
                grad_step_size=fast_learning_rate,
                hidden_nonlinearity=tf.nn.relu,
            )
            if bas == 'zero':
                baseline = ZeroBaseline(env_spec=env.spec)
            else:
                baseline = LinearFeatureBaseline(env_spec=env.spec)
            algo = SensitiveVPG(
                env=env,
                policy=policy,
                baseline=baseline,
                batch_size=5000, # use 100 trajs for grad update
                max_path_length=5,
                meta_batch_size=10,
                n_itr=200,
                use_sensitive=True,
                optimizer_args={'tf_optimizer_args':{'learning_rate': learning_rate}}
                #plot=True,
            )
            run_experiment_lite(
                algo.train(),
                n_parallel=1,
                snapshot_mode="last",
                seed=1,
                #exp_prefix='deleteme',
                #exp_name='deleteme'
                exp_prefix='sensitive1dT5_2017_01_19',
                exp_name='sensitive_flr_' + str(fast_learning_rate) + '_lr_' + str(learning_rate) + 'baseline_' + bas,
                #plot=True,
            )