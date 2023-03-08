This is a Python script that allows you to search for a specific text string on different onion search engines and save the results to a CSV file. The script uses the argparse module to parse command-line arguments.

To use the script, you need to run it from the command line and provide the following arguments:

--search or -s: The text you want to search for. This is a required argument.

--engine or -e: The search engines you want to use, separated by comma. If not specified, the script will use all available engines.

--output or -o: The name of the output file. If not specified, the script will use "search_onion.csv" as the default name.

Here is an example of how to run the script:

python onion_search.py --search "example search" --engine "haystak,grams,kraken" --output "my_search.csv"

The script will search for "example search" on the haystak, grams, and kraken search engines and save the results to a file called "my_search.csv".

Note that the script requires a running Tor service on your machine, listening on port 9050. If you don't have Tor installed, you can download it from the Tor Project website.
