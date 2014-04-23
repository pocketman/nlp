package semilardemo;

import java.util.HashMap;

/**
 *
 * @author Rajendra
 * Created on Jun 25, 2013, 2:39:32 PM 
 */
public class WordPair {
    public String word1;
    public String word2;
    public double gold;
    public String remarks;
    HashMap<String, Double> simScoreTable = new HashMap<>();
    
    public void setScore(String method, double value) {
        simScoreTable.put(method, value);
    }
    
    public HashMap<String, Double> getSimScoreTable() {
        return simScoreTable;
    }
}
