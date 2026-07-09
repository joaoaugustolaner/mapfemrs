from pathlib import Path

import httpx
import pytest

from src.extractors.sinan import Sinan


@pytest.fixture
def sinan_downloader(tmp_path):
    """
    Initializes parser with a temporary directory for output
    to avoid writing to your actual src/data/raw during tests.
    """
    sinan = Sinan()
    sinan.output_dir = tmp_path
    return sinan


def test_download(sinan_downloader, mocker):

    mock_date = mocker.patch('src.extractors.sinan.date')
    mock_date.today.return_value = mocker.Mock(year=2015)
    
    mock_sinan_class = mocker.patch('src.extractors.sinan.Sinan')
    mock_load_instance = mock_sinan_class.return_value.load.return_value

    mock_files_list = ["file_a.dbc", "file_b.dbc"]
    mock_load_instance.get_files.return_value = mock_files_list

    sinan_downloader.donwload()

    assert mock_sinan_class.called
    assert mock_sinan_class.return_value.load.called

    assert mock_load_instance.get_files.call_count == 3
    assert mock_load_instance.download.call_count == 3


    mock_load_instance.get_files.assert_any_call(
        'VIOL', 
        2014, 
        local_dir=sinan_downloader.output_dir
    )

    mock_load_instance.download.assert_called_with(mock_files_list)




    #INFO SENAC
    # 14 - 18 anos de idade
    # plano de aula recebido
    # 
