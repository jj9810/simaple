import simaple.simulate.component.skill  # pylint: disable=W0611
from simaple.core.damage import INTBasedDamageLogic
from simaple.simulate.actor import ActionRecorder, DefaultMDCActor
from simaple.simulate.component.view import (
    BuffParentView,
    RunningParentView,
    ValidityParentView,
)
from simaple.simulate.report.base import Report, ReportEventHandler
from simaple.simulate.report.dpm import DPMCalculator, LevelAdvantage


def test_actor(mechanic_client, character_stat):
    actor = DefaultMDCActor(
        order=[
            "로봇 마스터리",
            "호밍 미사일",
            "오픈 게이트: GX-9",
            "로봇 런처: RM7",
            "서포트 웨이버: H-EX",
            "마그네틱 필드",
            "로봇 팩토리: RM1",
            "봄버 타임",
            "윌 오브 리버티",
            "레지스탕스 라인 인팬트리",
            "디스토션 필드",
            "매시브 파이어: IRON-B",
        ]
    )
    events = []
    environment = mechanic_client.environment
    ValidityParentView.build_and_install(environment, "validity")
    BuffParentView.build_and_install(environment, "buff")
    RunningParentView.build_and_install(environment, "running")

    recorder = ActionRecorder("record.tsv")
    report = Report()

    mechanic_client.add_handler(ReportEventHandler(report))

    dpm_calculator = DPMCalculator(
        character_spec=character_stat,
        damage_logic=INTBasedDamageLogic(attack_range_constant=1.2, mastery=0.95),
        armor=300,
        level=LevelAdvantage().get_advantage(250, 260),
        force_advantage=1.5,
    )

    events = []
    with recorder.start() as rec:
        while environment.show("clock") < 50_000:
            action = actor.decide(mechanic_client.environment, events)
            events = mechanic_client.play(action)
            rec.write(action, environment.show("clock"))

    print(f"{environment.show('clock')} | {dpm_calculator.calculate_dpm(report):,} ")
    report.save("report.tsv")
