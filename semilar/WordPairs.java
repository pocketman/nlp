package semilardemo;

import java.util.ArrayList;
import semilar.utilities.io.FileReaderUtil;

/**
 *
 * @author Rajendra Created on Jun 25, 2013, 11:42:58 AM
 */
public class WordPairs {

    public static ArrayList<WordPair> getTestWordPairDataWithGoldStandard(String filePath) {
        ArrayList<WordPair> data = new ArrayList<>();
        //for demo purpose, using WordSim353 corpus, and there are only 318 (out of 353) pairs remained filtered out by TASA corpus and Wordnet vocabulary.
        ArrayList<String> lines = FileReaderUtil.getLinesFromFile(filePath);
        lines.remove(0);
        for (String line : lines) {
            line = line.toLowerCase();
            String[] splits = line.split(" ");
            WordPair instance = new WordPair();
            instance.word1 =splits[0];
            instance.word2 =splits[1];
            instance.gold = Double.parseDouble(splits[2]);
            data.add(instance);
        }
        return data;
    }
}
