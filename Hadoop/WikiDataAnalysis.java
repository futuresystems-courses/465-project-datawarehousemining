//This Program will count the no. of access to different wikidomains in the database

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.MapReduceCommand;
import com.mongodb.MapReduceOutput;
import com.mongodb.Mongo;


public class WikiDataAnalysis {

 public static void main(String[] args) {
  Mongo mongo;
  try {
//This will access mongo Db and collection  but will create if couldnt find 
   mongo = new Mongo("localhost", 27017);
   DB db = mongo.getDB("wikimedia_project");
   DBCollection pagecounts_small_May14 = db.getCollection("pagecounts_small_May14");

//creating and inserting data into collection using DB object

BasicDBObject wikidataobj= new BasicDBObject();
wikidataobj.put("year","2014");
wikidataobj.put("month","9");
wikidataobj.put("day","30");
wikidataobj.put("hour","23");
wikidataobj.put("domain","CA");
wikidataobj.put("page_title","yyyyyuvuvu.csv");
wikidataobj.put("count_views","66");
wikidataobj.put("total_response_size","4352");
pagecounts_small_May14.insert(wikidataobj);

wikidataobj= new BasicDBObject();
wikidataobj.put("year","2015");
wikidataobj.put("month","6");
wikidataobj.put("day","5");
wikidataobj.put("hour","5");
wikidataobj.put("domain","De");
wikidataobj.put("page_title","Datei:NeukÃ¶lln_Bweg_JohCh-FannyZobelBrÃ¼cke_P8250034_(3).JPG");
wikidataobj.put("count_views","5");
wikidataobj.put("total_response_size","5555");
pagecounts_small_May14.insert(wikidataobj);

wikidataobj= new BasicDBObject();
wikidataobj.put("year","2015");
wikidataobj.put("month","1");
wikidataobj.put("day","5");
wikidataobj.put("hour","5");
wikidataobj.put("domain","CA");
wikidataobj.put("page_title","Datei:NeukÃ¶lln_Bweg_JohCh-FannyZobelBrÃ¼cke_P8250034_(3).JPG");
wikidataobj.put("count_views","75");
wikidataobj.put("total_response_size","5885");
pagecounts_small_May14.insert(wikidataobj);

wikidataobj= new BasicDBObject();
wikidataobj.put("year","2015");
wikidataobj.put("month","3");
wikidataobj.put("day","2");
wikidataobj.put("hour","7");
wikidataobj.put("domain","AR");
wikidataobj.put("page_title","Ch-FannyZobelBrÃ¼cke_P8250034_(3).txt");
wikidataobj.put("count_views","3");
wikidataobj.put("total_response_size","35");
pagecounts_small_May14.insert(wikidataobj);

//This function will map domain to the  count of views  of pages under that domain

    String map1 = "function(){"+
 "           emit(this.domain, {Domain_Access_Count:this.count_views});"+
"}";

//This function will list all domains with the  total no. of  page views  under that domain in the complete collection i.e. total no. of time Domain accessed

String reduce1 = "function (key, values) { "+
    " total = 0; "+
    " for (var i in values) { "+
        " total += NumberInt(values[i].Domain_Access_Count); "+
    " } "+
    " return {Domain_Access_Count:total} }";

//This function will map page_title to the total count of page views 

 String map2 = "function(){"+
 "           emit(this.page_title, {Page_View_Count:this.count_views});"+
"}";

//This function will list all page_titles with the  total count of page views in the complete collection

String reduce2 = "function (key, values) { "+
    " total = 0; "+
    " for (var i in values) { "+
        " total +=NumberInt( values[i].Page_View_Count); "+
    " } "+    
" return {Page_View_Count:total} }";

//Calling map and reduce function for Domain access count
   MapReduceCommand cmd1 = new MapReduceCommand(pagecounts_small_May14, map1, reduce1,null, MapReduceCommand.OutputType.INLINE, null);
   MapReduceOutput out1 = pagecounts_small_May14.mapReduce(cmd1);
System.out.println("List of Domains and Total count of access");
   for (DBObject o1 : out1.results())
        {
         System.out.println(o1.toString());
         }

//Calling map and reduce function for page_title views count
 MapReduceCommand cmd2 = new MapReduceCommand(pagecounts_small_May14, map2, reduce2,null, MapReduceCommand.OutputType.INLINE, null);
   MapReduceOutput out2 = pagecounts_small_May14.mapReduce(cmd2);
       System.out.println("Page_title with total no. of view access");
    for (DBObject o2 : out2.results())
        {         System.out.println(o2.toString());
         }


  }
catch (Exception e) {

   // TODO Auto-generated catch block
   e.printStackTrace();
  }

 }
}

