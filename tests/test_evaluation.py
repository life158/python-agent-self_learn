import pytest

from src.evaluation import precision_at_k,recall_at_k,reciprocal_rank,mean_reciprocal_rank,evaluate_retrieval,convert_to_relevance

def test_precision_at_k():
    results = [1,0,1,0,0]
    result =  precision_at_k(results,4)
    assert result == 0.5

@pytest.mark.parametrize(
    "invalid_results",[[],"abc",[1,2,0],[1,True,0]]
)

def test_precision_at_k_invalid_results(invalid_results):
    with pytest.raises(ValueError):
        precision_at_k(invalid_results,4)


@pytest.mark.parametrize(
    "invalid_k",[0,-1,True,1.5]
)
def test_precision_at_k_invalid_k(invalid_k):
    with pytest.raises(ValueError):
        precision_at_k([1,0,1],invalid_k)

@pytest.mark.parametrize(
    "valid_k,expected",
    [
        (4,0.4),
        (3,0.4),
        (10,0.4)
    ]
)

def test_recall_at_k(valid_k,expected):
    results = [1,0,1,0]
    total_relevant = 5
    k = valid_k
    results = recall_at_k(results=results,k=valid_k,total_relevant=total_relevant)
    assert results == expected

#测试非法输入
#第一组:非法results
@pytest.mark.parametrize(
    "invalid_results",[[],"abc",[1,2,0,True,0]]
)
def test_recall_at_k_invalid_results(invalid_results):
    with pytest.raises(ValueError):
        recall_at_k(results=invalid_results,k=3,total_relevant=5)


#第二组:非法total_relevant
@pytest.mark.parametrize(
    "invalid_total_relevant",[0,-1,True,1.5]
)

def test_recall_at_k_invalid_total_relevant(invalid_total_relevant):
    with pytest.raises(ValueError):
        recall_at_k(results=[1,0,1,0],k=3,total_relevant=invalid_total_relevant)


#第三组：非法k
@pytest.mark.parametrize(
    "invalid_k",[0,-1,True,1.5]
)
def test_recall_at_k_invalid_k(invalid_k):
    with pytest.raises(ValueError):
        recall_at_k([1,0,1],k=invalid_k,total_relevant=5)

def test_recall_at_k_relevant_count_exceeds_total_relevant():
    with pytest.raises(ValueError):
        recall_at_k([1,1,1,0],k=4,total_relevant=2)


#测试reciprocal_rank
@pytest.mark.parametrize(
    "results,expected",
    [([1,0,0],1),
     ([0,1,0],0.5),
     ([0,0,1],1/3),
     ([0,0,0],0)
     ]
)
def test_reciprocal_rank(results,expected):
    result = reciprocal_rank(results)
    assert result == expected

#非法输入
@pytest.mark.parametrize(
    "invalid_results",[[],"abc",[1,2,0],[1,True,0]]
)

def test_reciprocal_rank_invalid_results(invalid_results):
    with pytest.raises(ValueError):
        reciprocal_rank(invalid_results)


def test_mean_reciprocal_rank():
    queries_results = [[1,0,0],[0,1,0],[0,0,0]]
    result = mean_reciprocal_rank(queries_results)
    assert result == 0.5


@pytest.mark.parametrize(
    "invalid_results",[[[0,0,0],[0,0,1],[0,2,0],[1,0,0]],[[0,0,0],[0,0,1],[0,1,0],[1,True,0]],[[],"abc",None]]
)
def test_mean_reciprocal_rank_invalid_results(invalid_results):
    with pytest.raises(ValueError):
        mean_reciprocal_rank(invalid_results)


def test_evaluate_retrieval():
    results = [1,0,1,0]
    total_relevant = 5
    k = 4
    result = evaluate_retrieval(results,k=k,total_relevant=total_relevant)
    assert result["precision_at_k"]==0.5
    assert result["recall_at_k"] == 0.4
    assert result["reciprocal_rank"]==1

#非法输入
@pytest.mark.parametrize(
    "invalid_results",[[],"abc",[1,2,0],[1,True,0]]
)

def test_evaluate_retrieval_invalid_results(invalid_results):
    with pytest.raises(ValueError):
        evaluate_retrieval(results=invalid_results,k=3,total_relevant=5)


@pytest.mark.parametrize(
    "invalid_k",[0,-1,True,1.5]
)
def test_evaluate_retrieval_invalid_k(invalid_k):
    with pytest.raises(ValueError):
        evaluate_retrieval(results=[1,0,1,0],k=invalid_k,total_relevant=5)


#测试convert_to_relevance()

#正常情况
def test_convert_to_relevant():
    retrieved_doc_ids = [
        "doc_001",
        "doc_001",
        "doc_002",
        "doc_003"
    ]

    relevant_doc_ids = [
        "doc_001",
        "doc_003"
    ]
    original_ids = retrieved_doc_ids.copy()

    assert convert_to_relevance(retrieved_doc_ids,relevant_doc_ids) ==[1,1,0,1]
    assert  retrieved_doc_ids == original_ids


#非法输入
@pytest.mark.parametrize(
    "invalid_retrieved_doc_ids",[[],"abc"]
)
def test_convert_to_relevant_invalid_retrieved_doc_ids(invalid_retrieved_doc_ids):
    with pytest.raises(ValueError):
        convert_to_relevance(invalid_retrieved_doc_ids,relevant_doc_ids=["doc_001"])


@pytest.mark.parametrize(
    "invalid_relevant_doc_ids",[[],"abc"]
)

def test_convert_to_relevant_invalid_relevant_doc_ids(invalid_relevant_doc_ids):
    with pytest.raises(ValueError):
        convert_to_relevance(retrieved_doc_ids=["doc_001", "doc_002", "doc_003"], relevant_doc_ids=invalid_relevant_doc_ids)
