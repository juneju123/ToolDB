from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier



class Learnings:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.dt_report = ""
        self.dt_predict = ""

    def decision_tree(self):
        self.decision_tree_clf = DecisionTreeClassifier(random_state=100)
        self.decision_tree_clf.fit(self.X_train, self.y_train)
        self.dt_predict = self.decision_tree_clf.predict(self.X_test)
        self.dt_report = classification_report(self.y_test, self.dt_predict)
        return self.dt_predict, self.dt_report

    def random_forest(self):
        self.random_forest_clf = RandomForestClassifier(n_estimators=100, random_state=1)
        self.random_forest_clf.fit(self.X_train, self.y_train)
        self.rf_predict = self.random_forest_clf.predict(self.X_test)
        self.rf_report = classification_report(self.y_test, self.rf_predict)
        return self.rf_predict, self.rf_report

    def k_neighbor(self):
        self.k_neighbor_clf = KNeighborsClassifier(n_neighbors=50,n_jobs=-1)
        self.k_neighbor_clf.fit(self.X_train, self.y_train)
        self.kn_predict = self.k_neighbor_clf.predict(self.X_test)
        self.kn_report = classification_report(self.y_test, self.kn_predict)
        return self.kn_predict, self.kn_report