
Tfbns is an open source python library for Binomial Seperation Feature Scaling. BNS is an improved feature representation over Term Frequency - Inverse Document Frequency (TFIDF) representation for SVM Text classification. The implementation of the library is based on the paper: "Forman, G. (2008, October). BNS feature scaling: an improved representation over tf-idf for svm text classification. In _Proceedings of the 17th ACM conference on Information and knowledge management_ (pp. 263-270)".

Usage:

    from tfbns.feature_extraction import tfbns

		df = pd.read_csv("data.csv")
		tfbns_vectorizer = Tfbns()
		x_train = df['text'].to_numpy()
		y_train = df['label'].to_numpy() 
		#Label should be binary containing 0 or 1
		x_train_tfbns = tfbns.fit_transform(x_train, y_train)
		x_test_tfbns = tfbns.transform(x_test)

