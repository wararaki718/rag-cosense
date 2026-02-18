import pytest
import torch
from unittest.mock import MagicMock, patch
from src.models.splade import SpladeModel

@patch("src.models.splade.AutoTokenizer")
@patch("src.models.splade.AutoModelForMaskedLM")
def test_splade_model_init(mock_model_cls, mock_tokenizer_cls):
    mock_tokenizer = MagicMock()
    mock_model = MagicMock()
    mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer
    mock_model_cls.from_pretrained.return_value = mock_model
    
    model = SpladeModel(model_id="test-model")
    
    assert model.model_id == "test-model"
    mock_tokenizer_cls.from_pretrained.assert_called_once_with("test-model")
    mock_model_cls.from_pretrained.assert_called_once_with("test-model")
    mock_model.to.assert_called_once()

@patch("src.models.splade.AutoTokenizer")
@patch("src.models.splade.AutoModelForMaskedLM")
def test_splade_model_encode(mock_model_cls, mock_tokenizer_cls):
    # Setup mocks
    mock_tokenizer = MagicMock()
    mock_model = MagicMock()
    mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer
    mock_model_cls.from_pretrained.return_value = mock_model
    
    # Mock tokenizer output
    mock_inputs = MagicMock()
    mock_inputs.to.return_value = {"input_ids": torch.tensor([[1, 2, 3]])}
    mock_tokenizer.return_value = mock_inputs
    mock_tokenizer.decode.side_effect = lambda x: f"token_{x[0]}"
    
    # Mock model output (logits)
    # Shape: (batch_size, seq_len, vocab_size)
    # Let's say batch_size=1, seq_len=3, vocab_size=5
    mock_logits = torch.zeros((1, 3, 5))
    # Fill some values to trigger SPLADE logic
    mock_logits[0, 0, 1] = 2.0  # token_1
    mock_logits[0, 1, 2] = 3.0  # token_2
    
    # Mock model call result
    mock_output = MagicMock()
    mock_output.logits = mock_logits
    mock_model.return_value = mock_output
    
    model = SpladeModel(model_id="test-model")
    model.device = torch.device("cpu") # ensure cpu for testing
    
    result = model.encode("test text")
    
    assert isinstance(result, dict)
    # SPLADE logic: torch.max(torch.log1p(torch.relu(logits)), dim=1)
    # token_1: max(log1p(2.0), 0, 0) -> log1p(2.0)
    # token_2: max(0, log1p(3.0), 0) -> log1p(3.0)
    
    assert "token_1" in result
    assert "token_2" in result
    assert result["token_1"] == pytest.approx(torch.log1p(torch.tensor(2.0)).item())
    assert result["token_2"] == pytest.approx(torch.log1p(torch.tensor(3.0)).item())

@patch("src.models.splade.AutoTokenizer")
@patch("src.models.splade.AutoModelForMaskedLM")
def test_splade_model_encode_special_tokens(mock_model_cls, mock_tokenizer_cls):
    """Test that special characters like dots and leading underscores are handled correctly."""
    # Setup mocks
    mock_tokenizer = MagicMock()
    mock_model = MagicMock()
    mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer
    mock_model_cls.from_pretrained.return_value = mock_model
    
    # Mock tokens
    # Token 1: "." -> should become "u_"
    # Token 2: "_admin" -> should become "u_admin"
    # Token 3: "abc.def" -> should become "abc_def"
    
    # Mock model output (logits)
    # Vocab size: 10
    mock_logits = torch.zeros((1, 1, 10))
    mock_logits[0, 0, 1] = 1.0  # token "."
    mock_logits[0, 0, 2] = 2.0  # token "_admin"
    mock_logits[0, 0, 3] = 3.0  # token "abc.def"
    
    mock_output = MagicMock()
    mock_output.logits = mock_logits
    mock_model.return_value = mock_output
    
    # Mock tokenizer mapping
    def mock_decode(token_ids):
        mapping = {
            1: ".",
            2: "_admin",
            3: "abc.def"
        }
        return mapping.get(token_ids[0], "unknown")
        
    mock_tokenizer.decode.side_effect = mock_decode
    mock_tokenizer.return_value.to.return_value = {"input_ids": torch.tensor([[1]])}
    
    model = SpladeModel(model_id="test-model")
    model.device = torch.device("cpu")
    
    result = model.encode("text")
    
    # Verify dot replacement and leading underscore handling
    assert "u_" in result, "Dot should be replaced by '_' and prefixed with 'u' because it starts with '_'"
    assert "u_admin" in result, "Leading underscore should be prefixed with 'u'"
    assert "abc_def" in result, "Dots in middle should be replaced with '_'"
    
    # Verify values are correct
    assert result["u_"] == pytest.approx(torch.log1p(torch.tensor(1.0)).item())
    assert result["u_admin"] == pytest.approx(torch.log1p(torch.tensor(2.0)).item())
    assert result["abc_def"] == pytest.approx(torch.log1p(torch.tensor(3.0)).item())
