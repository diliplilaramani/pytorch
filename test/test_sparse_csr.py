import torch

# NOTE: These tests are inspired from test_sparse.py and may duplicate some behaviour.
# Need to think about merging them both sometime down the line.

# Major differences between testing of CSR and COO is that we don't need to test CSR
# for coalesced/uncoalesced behaviour.

# TODO: remove this global setting
# Sparse tests use double as the default dtype
torch.set_default_dtype(torch.double)

import itertools
import functools
import random
import unittest
from torch.testing._internal.common_utils import TestCase, run_tests, load_tests

# load_tests from torch.testing._internal.common_utils is used to automatically filter tests for
# sharding on sandcastle. This line silences flake warnings
load_tests = load_tests

class TestSparseCSR(TestCase):
    def setUp(self):
        # These parameters control the various ways we can run the test.
        # We will subclass and override this method to implement CUDA
        # tests
        self.is_cuda = False
        self.is_uncoalesced = False
        self.device = 'cpu'
        self.exact_dtype = True
        self.value_dtype = torch.float64
        self.index_tensor = lambda *args: torch.tensor(*args, dtype=torch.int64, device=self.device)
        self.value_empty = lambda *args: torch.empty(*args, dtype=self.value_dtype, device=self.device)
        self.value_tensor = lambda *args: torch.tensor(*args, dtype=self.value_dtype, device=self.device)

        def sparse_tensor_factory(*args, **kwargs):
            kwargs['dtype'] = kwargs.get('dtype', self.value_dtype)
            kwargs['device'] = kwargs.get('device', self.device)
            return torch.sparse_csr_tensor(*args, **kwargs)
            
        self.sparse_tensor = sparse_tensor_factory
        super(TestSparseCSR, self).setUp()
    
    def test_csr_layout(self):
        self.assertEqual(str(torch.sparse_csr), 'torch.sparse_csr')
        self.assertEqual(type(torch.sparse_csr), torch.layout)

    def test_sparse_csr_constructor(self):
        # simple 1D tensor with shape inference
        pointers = torch.zeros(0)
        indices = self.index_tensor([1, 2, 3, 22, 39])
        values = self.values_tensor([33, 44, 55, 66, 77])
        a = self.csr_sparse_tensor(pointers, indices, values)

        self.assertEqual(a.layout, torch.sparse_csr)
        self.assertEqual(a.values(), values)
        self.assertEqual(a.indices(), indices)
        self.assertEqual(a.pointers(), pointers)
        self.assertEqual(a.ndimension(), 1)
        self.assertEqual(a.size(), torch.Size([40]))
        # simple 2D tensor with shape inference

        # simple 5D tensor with shape inference

        # simple 1D tensor with explicit shape
        pointers = torch.zeros(0)
        indices = self.index_tensor([1, 2, 3, 22, 39])
        values = self.values_tensor([33, 44, 55, 66, 77])
        a = self.csr_sparse_tensor(pointers, indices, values, [50])

        self.assertEqual(a.layout, torch.sparse_csr)
        self.assertEqual(a.values(), values)
        self.assertEqual(a.indices(), indices)
        self.assertEqual(a.pointers(), pointers)
        self.assertEqual(a.ndimension(), 1)
        self.assertEqual(a.size(), torch.Size([50]))

        # simple 2D tensor with explicit shape

        # simple 5D tensor with explicit shape

if __name__ == '__main__':
    run_tests()