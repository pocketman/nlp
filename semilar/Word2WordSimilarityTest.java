package semilardemo;

import java.util.ArrayList;
import java.util.HashMap;
import semilar.config.ConfigManager;
import semilar.data.Word;
import semilar.tools.preprocessing.SentencePreprocessor;
import semilar.tools.preprocessing.WordPreprocessor;
import semilar.tools.preprocessing.WordPreprocessor.StemmingTool;
import semilar.tools.semantic.WordNetSimilarity;
import semilar.utilities.io.FileWriterUtil;
import semilar.wordmetrics.LDAWordMetric;
import semilar.wordmetrics.LSAWordMetric;
import semilar.wordmetrics.PMIWordMetric;
import semilar.wordmetrics.WNWordMetric;

/**
 * Test program for SEMILAR API Word to word similarity/Relatedness measures.
 *
 * http://semanticsimilarity.org
 *
 * Please see other example code for largers texts (i.e. sentences and documents).
 *
 * @author Rajendra Created on Jul 5, 2013, 2:19:42 PM
 */
public class Word2WordSimilarityTest {

    ArrayList<WordPair> data;
    int limit = 99999; //process all pairs in the file by default.
    LSAWordMetric lsaMetricTasa;
    LDAWordMetric ldaMetricTasa;
    //PMIWordMetric pmiWordMetricWiki; --- Under review. Please contact SEMILAR team if you need PMI calculated from Whole Wiki.
    //WNWordMetric wnMetricLesk;
    WNWordMetric wnMetricLeskTanim;
    WNWordMetric wnMetricLeskTanimNoHyp;
    WNWordMetric wnMetricHso;
    WNWordMetric wnMetricJcn;
    WNWordMetric wnMetricLch;
    WNWordMetric wnMetricPath;
    WNWordMetric wnMetricRes;
    WNWordMetric wnMetricWup;
    WNWordMetric wnMetricLin;

    public Word2WordSimilarityTest(int limit, boolean wnFirstSenseOnly) {

        //LDA and LSA: Provide the LSA/LDA model name you want to use - STRING ? why no Enumeration for them?
        // Well, - you can create LSA and LDA models and use them - more limit, that's why no enumeration.
        lsaMetricTasa = new LSAWordMetric("LSA-MODEL-TASA-LEMMATIZED-DIM300");
        ldaMetricTasa = new LDAWordMetric("LDA-MODEL-TASA-LEMMATIZED-TOPIC300"); //provide the LDA model name you want to use.

        //Wordnet methods.
        wnMetricLeskTanim = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LESK_TANIM, wnFirstSenseOnly);
        wnMetricLeskTanimNoHyp = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LESK_TANIM_NOHYP, wnFirstSenseOnly);
        wnMetricHso = new WNWordMetric(WordNetSimilarity.WNSimMeasure.HSO, wnFirstSenseOnly);
        wnMetricJcn = new WNWordMetric(WordNetSimilarity.WNSimMeasure.JCN, wnFirstSenseOnly);
        wnMetricLch = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LCH, wnFirstSenseOnly);
        wnMetricPath = new WNWordMetric(WordNetSimilarity.WNSimMeasure.PATH, wnFirstSenseOnly);
        wnMetricRes = new WNWordMetric(WordNetSimilarity.WNSimMeasure.RES, wnFirstSenseOnly);
        wnMetricWup = new WNWordMetric(WordNetSimilarity.WNSimMeasure.WUP, wnFirstSenseOnly);
        wnMetricLin = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LIN, wnFirstSenseOnly);

        //calculate the similarity of this much number of word pairs. You may like to run for first few to see whether 
        //everything is fine (smoke test).
        this.limit = limit;
    }

    public void printSimScoreOnConsole(Word word1, Word word2, boolean useBaseForm) {
        String word1Str = useBaseForm ? word1.getBaseForm() : word1.getRawForm();
        String word2Str = useBaseForm ? word2.getBaseForm() : word2.getRawForm();
        
        System.out.println(word1Str + " " + word2Str);
        System.out.println("--------------------------------------------");
        System.out.println("WN-LESK_TANIM :" + wnMetricLeskTanim.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-LESK_TANIM_NOHYP :" + wnMetricLeskTanimNoHyp.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-HSO :" + wnMetricHso.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-JCN :" + wnMetricJcn.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-LCH: " + wnMetricLch.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-PATH :" + wnMetricPath.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-RES :" + wnMetricRes.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-WUP :" + wnMetricWup.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("WN-LIN :" + wnMetricLin.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("LSA-TASA: " + lsaMetricTasa.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("LDA-TASA: " + ldaMetricTasa.computeWordSimilarityNoPos(word1Str, word2Str));
        System.out.println("    ");
    }

    /**
     * Calculate similarity of word 2 word using various methods.
     *
     */
    public void calculateSimScoresDataFromFile(String inputFilePath) {
        int counter = 0;

        //read the word pairs from test file. Its your choice, either read from file or get them from somewhere else.
        // Please see the examples below.        
        data = WordPairs.getTestWordPairDataWithGoldStandard(inputFilePath);

        for (WordPair instance : data) {
            //instance.setScore("WN-LESK", wnMetricLesk.computeWordSimilarityNoPOS(instance.word1, instance.word2));
            instance.setScore("WN-LESK_TANIM", wnMetricLeskTanim.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-LESK_TANIM_NOHYP", wnMetricLeskTanimNoHyp.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-HSO", wnMetricHso.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-JCN", wnMetricJcn.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-LCH", wnMetricLch.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-PATH", wnMetricPath.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-RES", wnMetricRes.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-WUP", wnMetricWup.computeWordSimilarityNoPos(instance.word1, instance.word2));
            instance.setScore("WN-LIN", wnMetricLin.computeWordSimilarityNoPos(instance.word1, instance.word2));
            //LSA method
            instance.setScore("LSA-TASA", lsaMetricTasa.computeWordSimilarityNoPos(instance.word1, instance.word2));
            
            //LDA method.
            instance.setScore("LDA-TASA", ldaMetricTasa.computeWordSimilarityNoPos(instance.word1, instance.word2));
            counter++;
            if (counter >= limit) {
                System.out.println("Exiting... crossed the limit: " + limit);
                break;
            }
            if (counter % 20 == 0) {
                System.out.println("Processed " + counter + " pairs");
            }
        }
    }

    public void saveSimDataToFile(String fileName) {
        ArrayList<String> outLines = new ArrayList<>();
        for (WordPair instance : data) {
            String outLine = "";
            outLine += String.format("%15s\t%15s\t%2.3f", instance.word1, instance.word2, instance.gold);
            HashMap<String, Double> simTable = instance.getSimScoreTable();
            if (simTable.isEmpty()) {
                continue;
            }
            for (String methodName : simTable.keySet()) {
                outLine += String.format("\t%20s : %.3f", methodName, simTable.get(methodName));
            }
            outLines.add(outLine);
        }
        FileWriterUtil.writeToFile(outLines, fileName);
        System.out.println("Please see the similarity values in " + fileName);
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        int limit = 10;
        boolean wnFirstSenseOnly = false; //applies to wordnet based methods only.
        String wordPairInputFilePath;
        String similarityOutputFilePath;
        
        // first of all set the semilar data folder path (ending with /).
        ConfigManager.setSemilarDataRootFolder("C:/Users/<user-name>/data/semilar-data/");
       
        WordPreprocessor wordPreprocessor = new WordPreprocessor(StemmingTool.PORTER); //use porter stemmer.
        wordPreprocessor.initialize();
        Word2WordSimilarityTest wordSimCalculator = new Word2WordSimilarityTest(limit, wnFirstSenseOnly);

        //
        Word word1 = wordPreprocessor.preprocessWord("liquid");
        Word word2 = wordPreprocessor.preprocessWord("water");
        wordSimCalculator.printSimScoreOnConsole(word1, word2, false); //false means - use the raw form. Not the base (stem/lemma form).

        word1 = wordPreprocessor.preprocessWord("computerized");
        word2 = wordPreprocessor.preprocessWord("program");
        wordSimCalculator.printSimScoreOnConsole(word1, word2, false); //false means - use the raw form. Not the base (stem/lemma form).
        wordSimCalculator.printSimScoreOnConsole(word1, word2, true); //true means - use the base form (stem/lemma).
        
        //Read input data from file and write result to file.
        //Would you like to use wordnet first sense only ? set wnFirstSenseOnly = true; otherwise, maximum similarity among all senses is returned.        
        limit = 100; //process ? many pairs. set 99999  - process all pairs in the input file.
        wnFirstSenseOnly = false;
        wordPairInputFilePath = ConfigManager.getSemilarDataRootFolder() + "Word2Word-Similarity-test-data/WordSim318-Word2Word-sim-input.txt";
        similarityOutputFilePath = ConfigManager.getSemilarDataRootFolder() + "Word2Word-Similarity-test-data/WordSim318-Word2Word-sim-output.txt";
        //read the data from file, calculate the sim score
        wordSimCalculator.calculateSimScoresDataFromFile(wordPairInputFilePath);
        // and save the similarity score in the output file.
        wordSimCalculator.saveSimDataToFile(similarityOutputFilePath);

        System.out.println("Done!");
    }
}
