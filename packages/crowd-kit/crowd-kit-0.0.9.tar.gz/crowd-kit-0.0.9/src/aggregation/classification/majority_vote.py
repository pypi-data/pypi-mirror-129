__all__ = ['MajorityVote']

from typing import Optional

import attr

from .. import annotations
from ..annotations import Annotation, manage_docstring
from ..base import BaseClassificationAggregator
from ..utils import normalize_rows, get_most_probable_labels, get_accuracy, add_skills_to_data, named_series_attrib


@attr.s
@manage_docstring
class MajorityVote(BaseClassificationAggregator):
    """Majority Vote - chooses the correct label for which more performers voted"""

    # TODO: remove skills_
    skills_: annotations.OPTIONAL_SKILLS = named_series_attrib(name='skill')
    probas_: annotations.OPTIONAL_PROBAS = attr.ib(init=False)
    # labels_
    on_missing_skill: annotations.ON_MISSING_SKILL = attr.ib(default='error')
    default_skill: Optional[float] = attr.ib(default=None)

    @manage_docstring
    def fit(self, data: annotations.LABELED_DATA, skills: annotations.SKILLS = None) -> Annotation(type='MajorityVote', title='self'):
        data = data[['task', 'performer', 'label']]

        if skills is None:
            scores = data[['task', 'label']].value_counts()
        else:
            data = add_skills_to_data(data, skills, self.on_missing_skill, self.default_skill)
            scores = data.groupby(['task', 'label'])['skill'].sum()

        self.probas_ = normalize_rows(scores.unstack('label', fill_value=0))
        self.labels_ = get_most_probable_labels(self.probas_)
        self.skills_ = get_accuracy(data, self.labels_, by='performer')

        return self

    @manage_docstring
    def fit_predict_proba(self, data: annotations.LABELED_DATA, skills: annotations.SKILLS = None) -> annotations.TASKS_LABEL_PROBAS:
        return self.fit(data, skills).probas_

    @manage_docstring
    def fit_predict(self, data: annotations.LABELED_DATA, skills: annotations.SKILLS = None) -> annotations.TASKS_LABELS:
        return self.fit(data, skills).labels_
