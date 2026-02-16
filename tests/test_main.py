"""CLIのユニットテスト"""

from typer.testing import CliRunner

from screening_test.main import app


class TestCLI:
    """CLIコマンドのテスト"""

    def setup_method(self) -> None:
        self.runner = CliRunner()

    def test_version(self) -> None:
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "screening-test" in result.output
        assert "0.1.0" in result.output

    def test_help(self) -> None:
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "株式スクリーニングシステム" in result.output
