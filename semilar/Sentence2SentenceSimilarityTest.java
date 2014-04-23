import semilar.config.ConfigManager;
import semilar.data.Sentence;
import semilar.sentencemetrics.BLEUComparer;
import semilar.sentencemetrics.CorleyMihalceaComparer;
import semilar.sentencemetrics.DependencyComparer;
import semilar.sentencemetrics.GreedyComparer;
import semilar.sentencemetrics.LSAComparer;
import semilar.sentencemetrics.LexicalOverlapComparer;
import semilar.sentencemetrics.MeteorComparer;
import semilar.sentencemetrics.OptimumComparer;
import semilar.sentencemetrics.PairwiseComparer.NormalizeType;
import semilar.sentencemetrics.PairwiseComparer.WordWeightType;
import semilar.tools.preprocessing.SentencePreprocessor;
import semilar.tools.semantic.WordNetSimilarity;
import semilar.wordmetrics.LDAWordMetric;
import semilar.wordmetrics.LSAWordMetric;
import semilar.wordmetrics.WNWordMetric;
import semilar.wordmetrics.AbstractWordMetric;

import java.util.*;
import java.io.File;
import java.lang.Exception;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.*;

/**
 * Examples using various sentence to sentence similarity methods. Please note that due to huge models of similarity
 * measures (wordnet files, LSA model, LDA models, ESA, PMI etc) and preprocessors - Standford/OpenNLP models, you may
 * not be able to run all the methods in a single pass. Also, for LDA based methods, we have to estimate the topic
 * distributions for the candidate pairs before calculating similarity. So, The examples for LDA based sentence to
 * sentence similarity and document level similarity are provided in the separate file as they have special
 * requirements.
 *
 * Some methods calculate the similarity of sentences directly or some use word to word similarity expanding to the
 * sentence level similarity. See the examples + documentation for more details.
 *
 * @author Rajendra
 */
public class Sentence2SentenceSimilarityTest {

    /* NOTE:
     * The greedy matching and Optimal matching methods rely on word to word similarity method.
     *(please see http://aclweb.org/anthology//W/W12/W12-2018.pdf for more details). So, based on the unique word to
     * word similarity measure, they have varying output (literally, many sentence to sentence similarity methods from
     * the combinations).
     */
    //greedy matching (see the available word 2 word similarity in the separate example file). Here I use some of them
    // for the illustration.
    GreedyComparer greedyComparerWNLin; //greedy matching, use wordnet LIN method for Word 2 Word similarity
    GreedyComparer greedyComparerWNLeskTanim;//greedy matching, use wordnet LESK-Tanim method for Word 2 Word similarity
    GreedyComparer greedyComparerLSATasa; // use LSA based word 2 word similarity (using TASA corpus LSA model).
    GreedyComparer greedyComparerLDATasa; // use LDA based word 2 word similarity (using TASA corpus LDA model).
    //Overall optimum matching method.. you may try all possible word to word similarity measures. Here I show some.
    OptimumComparer optimumComparerWNLin;
    OptimumComparer optimumComparerWNLeskTanim;
    OptimumComparer optimumComparerLSATasa;
    OptimumComparer optimumComparerLDATasa;
    //dependency based method.. we need to provide a word to word similarity metric. Here is just one example
    // using Wordnet Lesk Tanim.
    DependencyComparer dependencyComparerWnLeskTanim;
    //Please see paper Corley, C. and Mihalcea, R. (2005). Measuring the semantic similarity of texts.
    CorleyMihalceaComparer cmComparer;
    //METEOR method (introduced for machine translation evaluation): http://www.cs.cmu.edu/~alavie/METEOR/
    MeteorComparer meteorComparer;
    //BLEU (introduced for machine translation evaluation):http://acl.ldc.upenn.edu/P/P02/P02-1040.pdf
    BLEUComparer bleuComparer;
    LSAComparer lsaComparer;
    LexicalOverlapComparer lexicalOverlapComparer; // Just see the lexical overlap.
    //For LDA based method.. see the separate example file. Its something different.

    public Sentence2SentenceSimilarityTest() {

        /* Word to word similarity expanded to sentence to sentence .. so we need word metrics */
        boolean wnFirstSenseOnly = false; //applies for WN based methods only.
        WNWordMetric wnMetricLin = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LIN, wnFirstSenseOnly);
        WNWordMetric wnMetricLeskTanim = new WNWordMetric(WordNetSimilarity.WNSimMeasure.LESK_TANIM, wnFirstSenseOnly);
        //provide the LSA model name you want to use.
        //LSAWordMetric lsaMetricTasa = new LSAWordMetric("LSA-MODEL-TASA-LEMMATIZED-DIM300");
        //provide the LDA model name you want to use.
        //LDAWordMetric ldaMetricTasa = new LDAWordMetric("LDA-MODEL-TASA-LEMMATIZED-TOPIC300");

        greedyComparerWNLin = new GreedyComparer(wnMetricLin, 0.3f, false);
        //greedyComparerWNLeskTanim = new GreedyComparer(wnMetricLeskTanim, 0.3f, false);
        //greedyComparerLSATasa = new GreedyComparer(lsaMetricTasa, 0.3f, false);
        //greedyComparerLDATasa = new GreedyComparer(ldaMetricTasa, 0.3f, false);

        optimumComparerWNLin = new OptimumComparer(wnMetricLin, 0.3f, false, WordWeightType.NONE, NormalizeType.AVERAGE);
        //optimumComparerWNLeskTanim = new OptimumComparer(wnMetricLeskTanim, 0.3f, false, WordWeightType.NONE, NormalizeType.AVERAGE);
        //optimumComparerLSATasa = new OptimumComparer(lsaMetricTasa, 0.3f, false, WordWeightType.NONE, NormalizeType.AVERAGE);
        //optimumComparerLDATasa = new OptimumComparer(ldaMetricTasa, 0.3f, false, WordWeightType.NONE, NormalizeType.AVERAGE);

        //Use one of the many word metrics. The example below uses Wordnet Lesk Tanim. Similarly, try using other
        //word similarity metrics.
        dependencyComparerWnLeskTanim = new DependencyComparer(wnMetricLeskTanim, 0.3f, true, "NONE", "AVERAGE");

        /* methods without using word metrics */
        cmComparer = new CorleyMihalceaComparer(0.3f, false, "NONE", "par");
        //for METEOR, please provide the **Absolute** path to your project home folder (without / at the end), And the
        // semilar library jar file should be in your project home folder.
        //meteorComparer = new MeteorComparer("C:/Users/Rajendra/workspace/SemilarLib/");
        bleuComparer = new BLEUComparer();

        //lsaComparer: This is different from lsaMetricTasa, as this method will
        // directly calculate sentence level similarity whereas  lsaMetricTasa
        // is a word 2 word similarity metric used with Optimum and Greedy methods.
        //lsaComparer = new LSAComparer("LSA-MODEL-TASA-LEMMATIZED-DIM300");
        //lexicalOverlapComparer = new LexicalOverlapComparer(false);  // use base form of words? - No/false.
        //for LDA based method.. please see the different example file.
    }

    public void printSimilarities(Sentence sentenceA, Sentence sentenceB) {
        System.out.println("Sentence 1:" + sentenceA.getRawForm());
        System.out.println("Sentence 2:" + sentenceB.getRawForm());
        System.out.println("------------------------------");
        System.out.println("greedyComparerWNLin : " + greedyComparerWNLin.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("greedyComparerWNLeskTanim : " + greedyComparerWNLeskTanim.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("greedyComparerLSATasa : " + greedyComparerLSATasa.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("greedyComparerLDATasa : " + greedyComparerLDATasa.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("optimumComparerWNLin : " + optimumComparerWNLin.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("optimumComparerWNLeskTanim : " + optimumComparerWNLeskTanim.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("optimumComparerLSATasa : " + optimumComparerLSATasa.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("optimumComparerLDATasa : " + optimumComparerLDATasa.computeSimilarity(sentenceA, sentenceB));
        System.out.println("dependencyComparerWnLeskTanim : " + dependencyComparerWnLeskTanim.computeSimilarity(sentenceA, sentenceB));
        System.out.println("cmComparer : " + cmComparer.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("meteorComparer : " + meteorComparer.computeSimilarity(sentenceA, sentenceB));
        System.out.println("bleuComparer : " + bleuComparer.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("lsaComparer : " + lsaComparer.computeSimilarity(sentenceA, sentenceB));
        //System.out.println("lexicalOverlapComparer : " + lexicalOverlapComparer.computeSimilarity(sentenceA, sentenceB));
        System.out.println("                              ");
    }
    public void readF(String f1, String f2, SentencePreprocessor p){
	ArrayList<Sentence> questions = new ArrayList<Sentence>();
	ArrayList<Sentence> sents = new ArrayList<Sentence>();
	try{
	    BufferedReader file1 = new BufferedReader(new FileReader(new File(f1)));
	    BufferedReader file2 = new BufferedReader(new FileReader(new File(f2)));
	    String text = null;
	    while((text = file1.readLine())!=null){
		questions.add(p.preprocessSentence(text));
	    }
	    System.out.println("======");
	    while((text = file2.readLine())!=null){
		sents.add(p.preprocessSentence(text));
	    }
	    file1.close();
	    file2.close();
	} catch (Exception e){
	    e.printStackTrace();
	}
	try{
	    BufferedWriter bw = new BufferedWriter(new FileWriter(new File("out")));
	    for (int i = 0; i<questions.size(); i++){
		for(int j = 0; j<sents.size(); j++){
		    Sentence q = questions.get(i);
		    Sentence s = sents.get(j);
		    double score = 0.4*cmComparer.computeSimilarity(q, s)+ 0.6*greedyComparerWNLin.computeSimilarity(q, s);
		    bw.write(Integer.toString(i)+"\t"+Integer.toString(j)+"\t"+score+"\n");
		}
	    }
	    bw.close();
	}catch(Exception e){
	    e.printStackTrace();
	}
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        // first of all set the semilar data folder path (ending with /).
        ConfigManager.setSemilarDataRootFolder("C:\\Users\\Ruixin\\Documents\\cmu\\spring2014\\NLP\\project\\SemilarExampleCodes\\data\\");
        SentencePreprocessor preprocessor = new SentencePreprocessor(SentencePreprocessor.TokenizerType.STANFORD, SentencePreprocessor.TaggerType.STANFORD, SentencePreprocessor.StemmerType.PORTER, SentencePreprocessor.ParserType.STANFORD);
        Sentence2SentenceSimilarityTest s2sSimilarityMeasurer = new Sentence2SentenceSimilarityTest();
	s2sSimilarityMeasurer.readF(args[0],args[1], preprocessor);

        System.out.println("\nDone!");
    }
}
