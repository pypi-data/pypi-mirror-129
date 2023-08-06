# -*- coding: utf-8 -*-
from __future__ import division
# Copyright (C) 2012 Matthew Hampton
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
from SpiffWorkflow import Task

from .BpmnSpecMixin import BpmnSpecMixin
from ...specs.SubWorkflow import SubWorkflow
from ...specs import TaskSpec


class CallActivity(SubWorkflow, BpmnSpecMixin):

    """
    Task Spec for a bpmn:callActivity node.
    """

    def __init__(self, wf_spec, name, bpmn_wf_spec=None, bpmn_wf_class=None,
                 **kwargs):
        """
        Constructor.

        :param bpmn_wf_spec: the BpmnProcessSpec for the sub process.
        :param bpmn_wf_class: the BpmnWorkflow class to instantiate
        """
        super(CallActivity, self).__init__(wf_spec, name, None, **kwargs)
        self.spec = bpmn_wf_spec
        self.wf_class = bpmn_wf_class
        self.sub_workflow = None

    def test(self):
        TaskSpec.test(self)

    def create_sub_workflow(self, my_task):

        sub_workflow = self.get_workflow_class()(
            self.spec, name=self.name,
            read_only=my_task.workflow.read_only,
            script_engine=my_task.workflow.outer_workflow.script_engine,
            parent=my_task.workflow)

        sub_workflow.completed_event.connect(
            self._on_subworkflow_completed, my_task)
        sub_workflow.data = my_task.workflow.data
        return sub_workflow

    def get_workflow_class(self):
        """
        Returns the workflow class to instantiate for the sub workflow
        """
        return self.wf_class

    def _on_subworkflow_completed(self, subworkflow, my_task):
        super(CallActivity, self)._on_subworkflow_completed(
            subworkflow, my_task)
        if isinstance(my_task.parent.task_spec, BpmnSpecMixin):
            my_task.parent.task_spec._child_complete_hook(my_task)

    def _on_ready_before_hook(self, my_task):
        self.sub_workflow = self.create_sub_workflow(my_task)
        self._integrate_subworkflow_tree(my_task, self.sub_workflow)

    def _on_ready_hook(self, my_task):
        # Assign variables, if so requested.
        for child in self.sub_workflow.task_tree.children:
            for assignment in self.in_assign:
                assignment.assign(my_task, child)

        self._predict(my_task)
        for child in self.sub_workflow.task_tree.children:
            child.task_spec._update(child)

    def serialize(self, serializer):
        return serializer.serialize_call_activity(self)
    @classmethod
    def deserialize(self, serializer, wf_spec, s_state):
        return serializer.deserialize_call_activity(wf_spec, s_state, CallActivity)



