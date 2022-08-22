from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
import matplotlib.pylab as plt


class Learnings:
    def __init__(self, X_train, X_test, y_train, y_test, fs):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.dt_report = ""
        self.dt_predict = ""
        self.fs = fs
        self.decision_tree_clf = DecisionTreeClassifier(random_state=200)
        self.random_forest_clf = RandomForestClassifier(n_estimators=100, random_state=3)
        self.k_neighbor_clf = KNeighborsClassifier(n_neighbors=50,n_jobs=3)

        if self.fs:
            self.selected_features = self.feature_selector()


    def decision_tree(self):
        self.decision_tree_clf.fit(self.X_train, self.y_train)
        self.dt_predict = self.decision_tree_clf.predict(self.X_test)
        self.dt_report = classification_report(self.y_test, self.dt_predict)
        return self.dt_predict, self.dt_report

    def random_forest(self):
        self.random_forest_clf.fit(self.X_train, self.y_train)
        self.rf_predict = self.random_forest_clf.predict(self.X_test)
        self.rf_report = classification_report(self.y_test, self.rf_predict)
        return self.rf_predict, self.rf_report

    def k_neighbor(self):
        self.k_neighbor_clf.fit(self.X_train, self.y_train)
        self.kn_predict = self.k_neighbor_clf.predict(self.X_test)
        self.kn_report = classification_report(self.y_test, self.kn_predict)
        return self.kn_predict, self.kn_report

    def feature_selector(self):
        sfs = SequentialFeatureSelector(self.decision_tree_clf, k_features=6, forward=True, floating=True,
                                        verbose=0,
                                        scoring='precision', cv=StratifiedKFold(3))
        sfs.fit(self.X_train, self.y_train)

        # Plot number of features VS. cross-validation scores
        plt.figure()
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation score (nb of correct classifications)")
        plt.plot([subset for subset in sfs.subsets_], [sfs.subsets_[subset]['avg_score'] for subset in sfs.subsets_])
        plt.show()
        self.X_train = self.X_train[list(sfs.k_feature_names_)]
        self.X_test = self.X_test[list(sfs.k_feature_names_)]
        return list(sfs.k_feature_names_)

    def plot_result(self, predict):
        plt.scatter(self.X_test.index.to_list(), self.y_test)
        plt.plot(self.X_test.index.to_list(), predict, color='Green')
        plt.show()



