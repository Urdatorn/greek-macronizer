import subprocess

working_directory = 'ifthimos'

command = ['ruby', 'test.rb']

# Run the Ruby script in the specified working directory
result = subprocess.run(command, cwd=working_directory, text=True, capture_output=True)

# Print the standard output and standard error of the Ruby script
print("Output:", result.stdout)
print("Error:", result.stderr)

# Execute a Ruby script from Python
#result = subprocess.run(['ruby', 'test.rb'], capture_output=True, text=True)
#print(result.stdout)