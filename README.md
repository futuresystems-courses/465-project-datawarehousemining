# 465-project-datawarehousemining

Our project aim is to process a large data set and to transform that data to give a more enhanced view for insight and decision-making. Specifically, we are using big data tools that will turn a raw dump of wikimedia project page visits into useful information.   Wikimedia projects consists of many popular web sites including Wikipedia, Mediawiki, wikibooks, etc.

Below procedure is followd for project implementatio

1. Take raw data of page view statistics from wikimedia https://dumps.wikimedia.org/other/pagecounts-raw/ Dataset is related to page view statistics across all Wikimedia sites (ie Wikipedia, wikibooks, Wikimedia, etc.)  with respect to hour, day, month and year
2. Create multi-node cluster using OpenStack (scalable and configurable)
3. Deploy mongodb to all nodes in cluster (positioned for future sharding across cluster)
4. Extract, transfer, and load datasets to one of the MongoDB instances
5. Create single node Hadoop cluster
6. Clustering of dataset using Map Reduce java program 
7. Execute on a virtual cluster
8. Output on command line
9. Single CM command for installation

## Installation

TODO: Describe the installation process

## Usage

TODO: Write usage instructions

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
