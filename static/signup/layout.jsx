class Index extends React.Component {
    render() {
        return (
            <div style={{textAlign: "center"}} id={"div" + this.props.idname} hidden>
                <h1 style={{fontSize: "2rem", marginBottom: "1vh"}}>{this.props.title}</h1>
                <input type="text" placeholder={this.props.placeholder} style={{marginBottom: "1vh", width: "230px"}} id={"input" + this.props.idname} type={this.props.type} /><br />
                <button id={this.props.idname} onClick={() => {next(this.props.idname)}}>확인</button>
            </div>
        )
    }
}

ReactDOM.render(
    <div>
        <Index title="이메일" placeholder="아이디로 사용됩니다." idname="1" type="email" />
        <Index title="닉네임" placeholder="실명은 입력하지 마세요." idname="2" type="email" />
        <Index title="비밀번호" placeholder="남들에게 알려주지 마세요." idname="3" type="password" />
        <Index title="비밀번호" placeholder="다시 비밀번호를 입력하세요..." idname="4" type="password" />
    </div>
, document.getElementById("root"))

document.getElementById(`div1`).hidden = false;