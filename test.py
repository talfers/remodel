import json
from app import main
from classes.files import Files

files = Files()

# TEST main()
with open("./property_data.json", "w") as outfile:
    outfile.write(json.dumps(main(files.read_json('./inputs.json')), indent=4))