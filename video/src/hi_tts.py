import json,sys,warnings;warnings.filterwarnings('ignore')
H='voice/hi/hi'
c=json.load(open(H+'/fastpitch/config.json'));sp=H+'/fastpitch/speakers.pth'
c['speakers_file']=sp
if 'model_args' in c: c['model_args']['speakers_file']=sp
json.dump(c,open(H+'/fastpitch/config_local.json','w'))
from TTS.utils.synthesizer import Synthesizer
s=Synthesizer(tts_checkpoint=H+'/fastpitch/best_model.pth',tts_config_path=H+'/fastpitch/config_local.json',vocoder_checkpoint=H+'/hifigan/best_model.pth',vocoder_config=H+'/hifigan/config.json',use_cuda=False)
if __name__=='__main__':
    print('speakers',s.tts_model.speaker_manager.speaker_names)
    jobs=json.load(open(sys.argv[1]))  # [[text, outpath],...]
    for text,out in jobs:
        w=s.tts(text,speaker_name='female');s.save_wav(w,out)
    print('done',len(jobs))
