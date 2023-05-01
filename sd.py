import importlib
import sys
import yaml

MODULES = {
  'txt': {
    'script': 'txt2img',
    'dir': 'scripts',
  },
  'img': {
    'script': 'img2img',
    'dir': 'scripts',
  },
  'gradio_depth': {
    'script': 'depth2img',
    'dir': 'scripts/gradio',
  },
  'gradio_inpainting': {
    'script': 'inpainting',
    'dir': 'scripts/gradio',
  },
  'gradio_superresolution': {
    'script': 'superresolution',
    'dir': 'scripts/gradio',
  },
  'streamlit_depth': {
    'script': 'depth2img',
    'dir': 'scripts/streamlit',
  },
  'streamlit_inpainting': {
    'script': 'inpainting',
    'dir': 'scripts/streamlit',
  },
  'streamlit_superresolution': {
    'script': 'superresolution',
    'dir': 'scripts/streamlit',
  },
  'streamlit_stableunclip': {
    'script': 'stableunclip',
    'dir': 'scripts/streamlit',
  },
}

# args = sys.argv[1:]

try:
  with open('config.user.yaml', 'r') as file:
    config = yaml.safe_load(file)

    try:
      input_module = sys.argv[1] or config['module']
    except:
      input_module = 'txt'

    try:
      for option in config['args']:
        if '--' + option not in sys.argv:
          sys.argv.extend(['--' + option, config['args'][option]])

    except Exception as e:
      print('Config parse error.')
      print(e)
      sys.exit()

except Exception as e:
  print('Invalid user config.\n')
  print(e)
  sys.exit()



try:
  module = MODULES[input_module]
except Exception as e:
  print('Invalid module.', e)
  sys.exit()

if __name__ == "__main__":
  prompt = input('Prompt:\n')
  sys.argv.extend(['--prompt', prompt])

  imported_module = importlib.import_module('.' + module['script'], module['dir'])

  opt = imported_module.parse_args()
  imported_module.main(opt)



