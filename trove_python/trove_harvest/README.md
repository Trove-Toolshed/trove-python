#basic-trove-harvester

A basic harvester for downloading records via the Trove API.

You'll want to subclass TroveHarvester and, at a minimum, overwrite process_results() to actually do something with the stuff you're harvesting.

Look in trove-theses for an example.