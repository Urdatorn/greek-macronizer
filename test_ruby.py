import subprocess

puts "Hello world!"

# Execute a Ruby script from Python
result = subprocess.run(['ruby', 'test.rb'], capture_output=True, text=True)
print(result.stdout)