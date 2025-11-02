import configparser

config = configparser.ConfigParser()
config.read('Python/config.ini')

# Access values
fontscale = config['settings'].getfloat('fontscale', 1.0)  # with default fallback
thickness = config['settings'].getint('thickness', 2)  # with default fallback
text_color = eval(config['settings'].get('text_color', '(255,255,255)'))  # with default fallback

print(f"Font Scale: {fontscale}, Thickness: {thickness}, Text Color: {text_color}")