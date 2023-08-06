function echov() {
  [ "$VERBOSE" = true ] && echo "$*"
} # echov

#-----------------------------------------------------------------------------------------------------------------------
function getConfig() {
  local PNAME=$1
  local CONFIG_FNAME=$CONF_DIR/pf.config
  if [ ! -f "$CONFIG_FNAME" ]; then echo "ERROR - config file '$CONFIG_FNAME' not found"; return 1; fi

  if [[ ! "${PYTHONPATH/$PF_ROOT/PF-LIB-IN-PATH}" =~ PF-LIB-IN-PATH ]]; then export PYTHONPATH="$PYTHONPATH:$PF_ROOT/lib"; fi
  /usr/bin/env python <<EOF
import configparser
import pi3dpf.pf_common as pfc
config         = configparser.ConfigParser(inline_comment_prefixes=';',
  empty_lines_in_values=False,
  converters={'list': lambda x: [i.strip() for i in x.split(',')]}) # cannot use interpolation=None, need to escape % (as %%) in values!
config.read('$CONFIG_FNAME')
print (pfc.get_config_param(config, '$PNAME'))
EOF
} # getConfig

#-----------------------------------------------------------------------------------------------------------------------
function getMainColorRGB() {
  local IMG_FNAME="$1"
  local PROP_FNAME="$2"
  /usr/bin/env python <<EO_PYTHON_PROG
import operator
from PIL import Image
image = Image.open('$IMG_FNAME')
count = {}
# count pixels per RGB color
for i in image.getdata():
  count[i] = count[i] + 1 if i in count.keys() else 1
maincolor = max(count.items(), key=operator.itemgetter(1))[0]
try:
  print("maincolor=rgb({},{},{})".format(maincolor[0], maincolor[1], maincolor[2]))
except IndexError as e:
  print('INFO - probably using this function on a transparent image $IMG_FNAME')
  exit(1)

# From: https://stackoverflow.com/a/44923761
# get first and last pixel not equal background 
rgb = image.convert('RGB')
x_min = image.size[0] + 1
x_max = -1
y_min = image.size[1] + 1
y_max = -1
r_min = maincolor[0] - 5
r_max = maincolor[0] + 5
g_min = maincolor[1] - 5
g_max = maincolor[1] + 5
b_min = maincolor[2] - 5
b_max = maincolor[2] + 5

for y in range(image.size[1]):
  for x in range(image.size[0]):
    rgb_pix = rgb.getpixel((x, y))
    if r_min <= rgb_pix[0] <= r_max and g_min <= rgb_pix[1] <= g_max and b_min <= rgb_pix[2] <= b_max:
      pass
    else:
      x_min = x if x < x_min else x_min
      x_max = x if x > x_max else x_max
      y_min = y if y < y_min else y_min
      y_max = y if y > y_max else y_max

print("x_min: {:4d} x_max: {:4d} y_min: {:4d} y_max: {:4d}\n".format(x_min, x_max, y_min, y_max))
#print("imagemagick_crop={}x{}+{}+{}".format(x_min, y_min, x_max - x_min, y_max - y_min))    
with open('$PROP_FNAME', 'w') as of:
  of.write("maincolor=rgb({},{},{})\n".format(maincolor[0], maincolor[1], maincolor[2]))
  of.write("imagemagick_crop={}x{}+{}+{}\n".format(x_max - x_min, y_max - y_min, x_min, y_min))
  of.write("x_min={}\n".format(x_min))
  of.write("x_max={}\n".format(x_max))
  of.write("y_min={}\n".format(y_min))
  of.write("y_max={}\n".format(y_max))
  
exit(0)
EO_PYTHON_PROG
#import pdb; pdb.set_trace()
} # getMainColorRGB

#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
function updateTemplateWithOWMdata() {
  local CONFIG_FNAME=$CONF_DIR/pf.config
  if [ ! -f "$CONFIG_FNAME" ]; then echo "ERROR - config file '$CONFIG_FNAME' not found"; return 1; fi
  /usr/bin/env python <<EO_PROGRAM
import pi3dpf.openweathermapToerikflowers_wi as owm
import libreoff2img as lofi

import configparser #, logger
import pi3dpf.pf_common as pfc
from pi3d import Log
logging = Log(level='INFO', format="%(asctime)s %(levelname)s: %(message)s") # name='a.py', 

config         = configparser.ConfigParser(inline_comment_prefixes=';',
                                           empty_lines_in_values=False,
                                           converters={'list': lambda x: [i.strip() for i in x.split(',')]}) # cannot use interpolation=None, need to escape % (as %%) in values!
config.read('$CONFIG_FNAME')

OWM_API_KEY          = pfc.get_config_param(config, 'OWM_API_KEY')
OWM_UNITS            = pfc.get_config_param(config, 'OWM_UNITS')
OWM_CITY_IDS         = pfc.get_config_param(config, 'OWM_CITY_IDS')
OWM_LOCAL_WEATHER_URL= pfc.get_config_param(config, 'OWM_LOCAL_WEATHER_URL')
OWM_LOCAL_WEATHER_URL+=OWM_API_KEY
logging.info('OWM_LOCAL_WEATHER_URL={}'.format(OWM_LOCAL_WEATHER_URL))

x = lofi.loff2img(config, logging)
x.addWeatherToTemplate()
EO_PROGRAM
}

