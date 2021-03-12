function next(id) {
    if (document.getElementById(`input${id}`).value.trim() !== "") {
        document.getElementById("div" + id).hidden = true;
        document.getElementById("div" + (Number(id) + 1)).hidden = false;
    }
}

class Index extends React.Component {
    render() {
        return (
            <div style={{textAlign: "center"}} id={"div" + this.props.divid} hidden>
                <h1 style={{fontSize: "2rem", marginBottom: "1vh"}}>{this.props.title}</h1>
                <input type="text" placeholder={this.props.placeholder} style={{marginBottom: "1vh"}} id={"input" + this.props.divid} type={this.props.type} /><br />
                <button id={this.props.divid} onClick={() => {next(this.props.divid)}}>확인</button>
            </div>
        )
    }
}

ReactDOM.render(
    <div>
        <Index title="계정 이메일" placeholder="이메일" divid="1" type="email" />
        <Index title="비밀번호" placeholder="비밀번호" divid="2" type="password" />
        <Index title="비밀번호" placeholder="다시 비밀번호를 입력하세요." divid="3" type="password" />
    </div>
, document.getElementById("root"))

document.getElementById(`div1`).hidden = false;