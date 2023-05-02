import importlib
import sys
import yaml


MODULE_PATHS = {
  'txt': {
    'module': 'txt2img',
    'path': 'scripts/txt2img.py',
  },
  'img': {
    'module': 'img2img',
    'path': 'scripts/img2img.py',
  },
  'depth': {
    'module': 'depth2img',
    'path': 'scripts/gradio/depth2img.py',
  },
  'inpainting': {
    'module': 'inpainting',
    'path': 'scripts/gradio/inpainting.py',
  },
  'superresolution': {
    'module': 'superresolution',
    'path': 'scripts/gradio/superresolution.py',
  },
  'streamlit_depth': {
    'module': 'depth2img',
    'path': 'scripts/streamlit/depth2img.py',
  },
  'streamlit_inpainting': {
    'module': 'inpainting',
    'path': 'scripts/streamlit/inpainting.py',
  },
  'streamlit_superresolution': {
    'module': 'superresolution',
    'path': 'scripts/streamlit/superresolution.py',
  },
  'streamlit_stableunclip': {
    'module': 'stableunclip',
    'path': 'scripts/streamlit/stableunclip.py',
  },
}

try:
  with open('config.user.yaml', 'r') as file:
    user_config = yaml.safe_load(file)

    try:
      input_module = sys.argv[1] or user_config['module']
    except:
      input_module = 'txt'

    try:
      module_config = user_config[input_module]

      for option in module_config['args']:
        value = module_config['args'][option]

        if '--' + option not in sys.argv and value is not None:
          sys.argv.extend(['--' + option, value])

    except Exception as e:
      print('Config parse error.')
      print(e)
      sys.exit()

except Exception as e:
  print('Invalid user config.\n')
  print(e)
  sys.exit()


try:
  module = MODULE_PATHS[input_module]

except Exception as e:
  print('Invalid module.', e)
  sys.exit()

for arg in sys.argv:
  if arg in MODULE_PATHS:
    sys.argv.remove(arg)


print(sys.argv)


def main():
  if 'prompt' in module_config['args']:
    prompt = input('Prompt:\n')
    prompt = prompt.strip()

    if prompt is not None:
      sys.argv.extend(['--prompt', prompt])


  spec = importlib.util.spec_from_file_location(module['module'], module['path'])
  imported_module = importlib.util.module_from_spec(spec)
  sys.modules[module['module']] = imported_module
  spec.loader.exec_module(imported_module)
  # imported_module = importlib.import_module(module['module'])

  try:
    if imported_module.parse_args is not None:
      opt = imported_module.parse_args()
      imported_module.main(opt)
      return

  except:
    pass

  imported_module.main()


if __name__ == "__main__":
  main()




