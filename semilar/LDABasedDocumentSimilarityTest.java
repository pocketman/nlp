package semilardemo;

import semilar.sentencemetrics.IRADComparer;
import semilar.tools.lda.LDAInferencer;

/**
 * Measuring documents similarity based on LDA is something different from others and we have created separate example
 * code file for it. It is different in the sense that you just can't provide two sentences (or documents), and get the
 * similarity score. It is a two phase process, first, infer the probability distributions (including document
 * distributions over topics) for your documents and provide the distributions to get the similarity.
 *
 * Main steps:
 *
 * 1. We need LDA model to infer the probability distributions of new documents to be able to calculate the similarity.
 * You may use the LDA models available in the SEMILAR website or you can generate LDA model using your document
 * collections. Please see LDA Test code for the examples how to generate LDA model from your documents.
 *
 * 2. Keep the LDA model files (<model name>.info, .theta,.phi,.tasign,.twords) in a folder (we would suggest you create
 * new folder for cleanness).
 *
 * 3. Create input file. Keep a document in a separate line (document may contain one sentence or many but keep them in
 * a single line each). You may be trying to measure the similarity of sentences but we still call each line a document.
 * And put the total number of documents in the first line (see exmple input file).
 *
 * 4. Infer the probability distributions for the documents provided inthe input file. (please see the example code
 * below). OR if you have already inferred the probability distributions for your documents, skip this step.
 *
 * 5. Measure the document similarity. Lets say, document-5 and document-6 (similarity of texts in 6th line and 7th
 * line. Note that first line is excluded in counting as it is just the total number of documents in the input file).
 * Provide the document distribution over topics (<input file name>.<model name>.theta), and document ids.
 *
 * 6. Method used to calculate the similarity is Information Radius. Please see the following paper (the method which
 * was used to assess the paraphrase is applicable to larger texts as well),
 *
 * Rus, Vasile, Nobal Niraula, and Rajendra Banjade. "Similarity Measures Based on Latent Dirichlet Allocation."
 * Computational Linguistics and Intelligent Text Processing. Springer Berlin Heidelberg, 2013. 459-470
 *
 * About the LDA tool: Xuan-Hieu Phan, Le-Minh Nguyen, and Susumu Horiguchi. Learning to Classify Short and Sparse Text
 * & Web with Hidden Topics from Large-scale Data Collections. In Proc. of The 17th International World Wide Web
 * Conference (WWW 2008), pp.91-100, April 2008, Beijing, China
 *
 * @author Rajendra Created on Jul 28, 2013, 9:25:34 AM
 */
public class LDABasedDocumentSimilarityTest {

    String ldaDataFolder = "C:\\Users\\Rajendra\\data\\semilar-data\\LDA-tool-test-data";
    //use the following model (the LDA model files .theta, .beta etc are named with the model name).
    String modelName = "LDA-Test-Model";

    public void doLDAInference(String inputFileNameInferer) {
        //Inferencing..
        LDAInferencer ldaInferer = new LDAInferencer(ldaDataFolder, inputFileNameInferer, modelName);
        ldaInferer.startInferencing();
        System.out.println("Please see the " + ldaDataFolder + " folder for the inferred distributions. File names end with model name!");
    }

    public static void main(String[] args) {

        //The following two lines infer the probability distributions for your documents.
        LDABasedDocumentSimilarityTest ldaBasedSimilarity = new LDABasedDocumentSimilarityTest();
        ldaBasedSimilarity.doLDAInference("ulpc_train_lda_preprocessed.txt");

        // Please make sure that document distribution over topics exists.
        String thetaFile = "C:\\Users\\Rajendra\\data\\semilar-data\\LDA-tool-test-data\\ulpc_train_lda_preprocessed.txt.LDA-Test-Model.theta";

        //LDA based similarity measurer : Information radius method (IRAD).
        IRADComparer comparer = new IRADComparer(thetaFile);
        //calculate the similarity of 5th and 6th document (i.e. documents in 6th and 7th line in your input file as first line is the total number of
        // documents in your input file.
        double simScore = comparer.calculateSimilarity(5, 6);

        System.out.println("Similarity score is :" + simScore);

        System.out.println("Done!");

    }
}
