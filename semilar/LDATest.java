package semilardemo;

import semilar.tools.lda.LDAEstimator;
import semilar.tools.lda.LDAInferencer;

/**
 * Please understand the LDA model estimation and Inferencing process first.
 *
 * NOTE: If you want to use the LDA models available in SEMILAR website, you can skip the estimation step and go to inferencing
 * step (see below).
 *
 * For any issues, questions, helps - please fell free to contact SEMILAR team.
 *
 * @author Rajendra (rbanjade@memphis.edu) Created on May 30, 2013, 6:18:56 PM
 */
public class LDATest {
    //folder where the input file for model Estimator is.. and 
    // the model files will be created on the same folder.

    String ldaDataFolder = "C:\\Users\\<user-name>\\data\\semilar-data\\LDA-tool-test-data";
    // The model files will be created with this name. And if you do the inferencing, model name will be appended in the
    // output files.
    String modelName = "LDA-Test-Model";

    /**
     * Estimation.. by default, the number of topics is set to 300. //if you would you like to change the model
     * parameters, see the other setters in ldaEstimator (below).
     *
     * @param inputFileNameEstimator
     */
    public void doLDAEstimation(String inputFileNameEstimator) {

        LDAEstimator ldaEstimator = new LDAEstimator(ldaDataFolder, inputFileNameEstimator, modelName);
        ldaEstimator.setNumberOfIterations(1000);
        ldaEstimator.startEstimation();

        System.out.println("Please see the " + ldaDataFolder + " folder for the generated model files!");
    }

    /**
     * Once you have LDA model (either you generated yourself or downloaded from the SEMILAR website
     * (semanticsimilarity.org), you can infer the distributions.
     *
     * @param inputFileNameInferer
     */
    public void doLDAInference(String inputFileNameInferer) {
        //Inferencing..
        LDAInferencer ldaInferer = new LDAInferencer(ldaDataFolder, inputFileNameInferer, modelName);
        ldaInferer.startInferencing();
        System.out.println("Please see the " + ldaDataFolder + " folder for the inferred distributions. File names end with model name!");
    }

    public static void main(String[] args) {


        // Input file for the model estimator.. (i.e. LDA model is created from this file).
        // Please make sure that the format of input text is correct.
        // First line contains the total number of documents (i.e. line) in the file.
        // Document may be a single sentence, or bigger texts but always put in a single line.
        // Each line is termed as document no matter how long the document size is.
        String inputFileNameEstimator = "msrp_test_lda_preprocessed.txt";


        // Input file for the inferencing 
        // Please make sure that the format of input text is correct.
        // First line contains the total number of documents (i.e. line) in the file.
        // Document may be a single sentence, or bigger texts but always put in a single line.
        // Each line is termed as document no matter how long the document size is.
        // the output files will contain this file name plus the model name.
        String inputFileNameInferer = "ulpc_train_lda_preprocessed.txt";


        LDATest ldaTest = new LDATest();
        ldaTest.doLDAEstimation(inputFileNameEstimator);
        ldaTest.doLDAInference(inputFileNameInferer);

        System.out.println("Done!");
    }
}
