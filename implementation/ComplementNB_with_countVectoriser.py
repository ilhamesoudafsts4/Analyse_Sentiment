import numpy as np
import pandas as pd
import sklearn.metrics as mt
from tabulate import tabulate
from matplotlib import pyplot as plt
import sklearn.model_selection as ms
#from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

filename = 'C:/Users/net/Desktop/sentiment-analysis-master/sentiment-analysis/datasets/amazon_unlocked_mobile_datasets_with_sentiment.csv'
names = ['product.name', 'brand.name', 'review.text', 'review.process', 'review.tokened', 'score', 'sentiment']
fields = ['review.tokened', 'sentiment']
review = pd.read_csv(filename, names=names, usecols=fields)
print('split data --- start')
array = review.values
X = array[:, 0:1]
Y = array[:, 1]
size = 0.3
trainX, testX, trainY, testY = ms.train_test_split(X, Y, test_size=size, shuffle=True)
print('split data --- end')

tv = TfidfVectorizer(use_idf=True, min_df=0.0, max_df=1.0, ngram_range=(1, 2), sublinear_tf=False, stop_words='english')
tv_train = tv.fit_transform(trainX.ravel())
tv_test = tv.transform(testX.ravel())  # transform test review into features
from sklearn.naive_bayes import ComplementNB
CNB = ComplementNB()
CNB.fit(tv_train, trainY)

mnb_pred = CNB.predict(tv_test)  # predict using model
print('prediction --- end')



print('\nModel Evaluation:')
mnb_accuracy = np.round(mt.accuracy_score(testY, mnb_pred), 3)
mnb_precision = np.round(mt.precision_score(testY, mnb_pred, average='macro'), 3)
mnb_recall = np.round(mt.recall_score(testY, mnb_pred, average='macro'), 3)
mnb_f1 = np.round(mt.f1_score(testY, mnb_pred, average='macro'), 3)

tv_metrics = np.array([mnb_accuracy, mnb_precision, mnb_recall, mnb_f1])
tv_metrics = pd.DataFrame([tv_metrics], columns=['accuracy', 'precision', 'recall', 'f1'], index=['metrics'])
print('Performance Metrics:')
print(tabulate(tv_metrics, headers='keys', tablefmt='github'))

# visualization
fig = plt.figure()
ax = tv_metrics.plot.bar()
plt.title('Machine Learning Approach Performance Evaluation\n')
plt.ylabel('result')
plt.xlabel('model evualtion')
plt.xticks(rotation=-360)  # rotate x labels
plt.ylim([0.1, 1.0])
for item in ax.patches:  # show value on plot
    ax.annotate(np.round(item.get_height(), decimals=2), (item.get_x() + item.get_width() / 2., item.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
plt.savefig('C:/Users/net/Desktop/sentiment-analysis-master/sentiment-analysis/results/ml_performance.png', format='png', transparent=False)  # save result
plt.show()


print('\nConfusion Matrix of Machine Learning Approach:\n')

# display and plot confusion matrix
labels = ['positive', 'negative', 'neutral']
cv_cm = mt.confusion_matrix(testY, mnb_pred, labels=labels)

# plot
# references: https://stackoverflow.com/questions/19233771/sklearn-plot-confusion-matrix-with-labels/48018785
# display and plot confusion matrix
tv_cm = mt.confusion_matrix(testY, mnb_pred, labels=labels)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.title('Confusion Matrix of Machine Learning Approach\n')
fig.colorbar(ax.matshow(tv_cm))
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('predicted')
plt.ylabel('true')
plt.savefig('../results/ml_confusion_matrix.png', format='png', transparent=False)  # save result
plt.show()

# display in table format
level = [len(labels)*[0], list(range(len(labels)))]
tv_cmf = pd.DataFrame(data=tv_cm,
                      columns=pd.MultiIndex(levels=[['predicted:'], labels], labels=level),
                      index=pd.MultiIndex(levels=[['actual:'], labels], labels=level))
print(tv_cmf)

print('\nClassification Report of MultinomialNB with TF-IDF Feature Extraction:\n')

# classification report for machine learning
tv_report = mt.classification_report(testY, mnb_pred, labels=labels)
print(tv_report)

print()

# output performance to csv
tv_metrics.to_csv('../results/ml_performance_result.csv', index=None, header=True)

# end of ml sentiment analysis

"""
Appendix
"""
# # feature extraction
# # build bag of world feature and tfidf feature on train reviews
# # reference: https://stackoverflow.com/questions/18200052/how-to-convert-ndarray-to-array
# print('feature extraction --- start')
# cv = CountVectorizer(binary=False, min_df=0.0, max_df=1.0, ngram_range=(1, 2))
# cv_train = cv.fit_transform(trainX.ravel())
# cv_test = cv.transform(testX.ravel())  # transform test review into features

# # multinomial naive bayes predict on bow
# mnb = MultinomialNB()
# mnb.fit(tv_train, trainY)  # build model
# tv_pred = mnb.predict(tv_test)  # predict using model
# print('prediction --- end')

# # prediction
# print('\nModel Evaluation with Bag of Word:')
# cv_accuracy = np.round(mt.accuracy_score(testY, cv_pred), 2)
# cv_precision = np.round(mt.precision_score(testY, cv_pred, average='macro'), 2)
# cv_recall = np.round(mt.recall_score(testY, cv_pred, average='macro'), 2)
# cv_f1 = np.round(mt.f1_score(testY, cv_pred, average='macro'), 2)
#
# cv_metrics = np.array([cv_accuracy, cv_precision, cv_recall, cv_f1])
# cv_metrics = pd.DataFrame([cv_metrics], columns=['accuracy', 'precision', 'recall', 'f1'], index=['bag of word'])
# print('Performance Metrics:')
# print(tabulate(cv_metrics, headers='keys', tablefmt='github'))

# # display and plot confusion matrix of bag-of-word
# labels = ['positive', 'negative', 'neutral']
# cv_cm = mt.confusion_matrix(testY, cv_pred, labels=labels)
# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.title('Confusion Matrix of MultinomialNB with Bag of Word Feature Extraction\n')
# fig.colorbar(ax.matshow(cv_cm))
# ax.set_xticklabels([''] + labels)
# ax.set_yticklabels([''] + labels)
# plt.xlabel('predicted')
# plt.ylabel('true')
# plt.show()
#
# # display in table format
# level = [len(labels)*[0], list(range(len(labels)))]
# cv_cmf = pd.DataFrame(data=cv_cm,
#                       columns=pd.MultiIndex(levels=[['predicted:'], labels], labels=level),
#                       index=pd.MultiIndex(levels=[['actual:'], labels], labels=level))
# print(cv_cmf)

# print('\nConfusion Matrix of MultinomialNB with Bag of Word Feature Extraction:\n')
#
# # classification report for bag-of-word
# cv_report = mt.classification_report(testY, cv_pred, labels=labels)
# print(cv_report)
