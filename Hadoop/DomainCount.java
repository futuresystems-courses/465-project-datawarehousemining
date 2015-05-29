//This Program will count the no. of access to different wikidomains in the database

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBObject;
import com.mongodb.MapReduceCommand;
import com.mongodb.MapReduceOutput;
import com.mongodb.Mongo;


public class DomainCount {

 public static void main(String[] args) {
  Mongo mongo;
  try {
   mongo = new Mongo("localhost", 27017);
   DB db = mongo.getDB("wikimedia_project");
   DBCollection pagecounts_small_May14 = db.getCollection("pagecounts_small_May14");

//This function will map domain to the  count of views  of pages under that domain

    String map = "function(){"+
 "           emit(this.domain, {Domain_Access_Count:this.count_views});"+
"}";

//This function will list all domains with the  total no. of  page views  under that domain in the complete collection i.e. total no. of time Domain accessed

String reduce = "function (key, values) { "+
    " total = 0; "+
    " for (var i in values) { "+
        " total += values[i].Domain_Access_Count; "+
    " } "+
    " return {Domain_Access_Count:total} }";

   MapReduceCommand cmd = new MapReduceCommand(pagecounts_small_May14, map, reduce,null, MapReduceCommand.OutputType.INLINE, null);
   MapReduceOutput out = pagecounts_small_May14.mapReduce(cmd);
   for (DBObject o : out.results())
        {
         System.out.println(o.toString());
         }
  }
catch (Exception e) {

   // TODO Auto-generated catch block
   e.printStackTrace();
  }

 }
}

