import numpy as np
import utils
import retrieval_run
import settings


# ============================================================
# 1. Instrument Configuration
# ============================================================

wavelength_range = [0.996, 2.508]
R_file = './examples/example_data/G570D_R_file.txt'
fwhm = 555

obspec = np.asfortranarray(
    np.loadtxt(
        './examples/example_data/G570D_2MHcalib.dat',
        dtype="d",
        unpack=True
    )
)


instrument_instance = utils.Instrument(
    wavelength_range=wavelength_range,
    R_file=R_file,
    obspec=obspec,
    fwhm=fwhm
)


# ============================================================
# 2. Model Configuration
# ============================================================

samplemode = 'mcmc'

do_fudge = 1


model_config_instance = utils.ModelConfig(
    samplemode=samplemode,
    do_fudge=do_fudge,
    malk=1,
    mch4=0,
    do_bff=0,
    cloudpath='../Clouds_V2/',
    xpath='../Linelists/',
    xlist='./data/gaslistR10K.dat',
    dist=5.84
)


# ============================================================
# 3. I/O Configuration
# ============================================================

io_config_instance = utils.IOConfig(
    runname='G570D_V2',
    outdir='../Saves/G570D/test/',
    runtest=1
)


# ============================================================
# 4. Retrieval Parameter Configuration
# ============================================================

chemeq = 0

gaslist = ['h2o', 'co', 'co2', 'ch4', 'nh3', 'h2s', 'k', 'na']

gastype_list = ['U', 'U', 'U', 'U', 'U', 'U', 'U', 'U']

ptype = 2

do_clouds = 0

npatches = 1

cloud_name = None

cloud_type = None

cloudpatch_index = None

particle_dis = None


re_params = utils.Retrieval_params(
    samplemode=samplemode,
    chemeq=chemeq,
    gaslist=gaslist,
    gastype_list=gastype_list,
    do_fudge=do_fudge,
    ptype=ptype,
    do_clouds=do_clouds,
    npatches=npatches,
    cloud_name=cloud_name,
    cloud_type=cloud_type,
    cloudpatch_index=cloudpatch_index,
    particle_dis=particle_dis,
    instrument=instrument_instance,
    vrad=False,
    vsini=False,
    fwhm=fwhm
)


# ============================================================
# 5. Generate Retrieval Arguments
# ============================================================

args_instance = utils.ArgsGen(
    re_params,
    model_config_instance,
    instrument_instance,
    obspec
)


settings.init(args_instance)


# ============================================================
# 6. Prior Settings
# ============================================================

re_params.dictionary['gas']['h2o']['params']['log_abund']['MC_init_dis']=['normal',-3.5,0.5]
re_params.dictionary['gas']['nh3']['params']['log_abund']['MC_init_dis']=['normal',-4.8,0.5]
re_params.dictionary['gas']['h2s']['params']['log_abund']['MC_init_dis']=['normal',-8.0,0.5]
re_params.dictionary['gas']['K_Na']['params']['log_abund']['MC_init_dis']=['normal',-5.5,0.5]
re_params.dictionary['refinement_params']['params']['logg']['MC_init_dis']=['normal',4.9,0.1]


# ============================================================
# 7. Start Retrieval
# ============================================================

retrieval_run.brewster_reterieval_run(
    re_params,
    model_config_instance,
    io_config_instance
)
