import sys
sys.path.insert(0, '..')

print('Testing imports...')
try:
    import weather
    print('Weather imported successfully')
except Exception as e:
    print(f'Weather import failed: {e}')

try:
    import test_weather
    print('Test weather imported successfully')
except Exception as e:
    print(f'Test weather import failed: {e}')