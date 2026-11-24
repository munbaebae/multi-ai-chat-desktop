#!/usr/bin/env python3
"""Add Korean localization to Multi-AI Chat Desktop.

Target: TED-H-com/multi-ai-chat-desktop, upstream main at 4156b9438474de466b9d00a37e7fbfd4007691bf.
Usage: python apply_korean.py [repository-directory] [--check]
No network access, dependency installation, Git commits, or pushes are performed.
The original MIT license and notices in the target repository must be retained.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TRANSLATIONS = r'''
mode.free.name|동시 질문
mode.debate.name|토론
mode.consult.name|자문
mode.coding.name|코딩
mode.roundtable.name|원탁회의
preset.catalog.aria|협업 모드 목록
preset.free.displayName|동시 질문
preset.free.meta|1분 미만
preset.free.description|선택한 AI에게 질문하여 빠르게 독립적인 답변을 받습니다. 답변을 비교하거나 다른 의견을 확인할 때 적합합니다.
preset.free.costLabel|선택한 AI · 1분 미만 · 낮은 RAM 사용량
preset.debate.displayName|토론
preset.debate.meta|약 4분
preset.debate.description|찬반 논거와 중립적인 종합 판단이 필요한 질문에 사용합니다. 찬성, 반대, 심사, 종합 단계를 진행합니다.
preset.debate.costLabel|4개 역할 · 4개 로그인 · 3~5분 · 보통 RAM 사용량
preset.consult.displayName|자문
preset.consult.meta|약 2분
preset.consult.description|조사 및 분석이 필요한 질문에 사용합니다. 두 역할이 먼저 답변하고, 검토자가 확인한 뒤 최종 단계에서 간결한 종합 답변을 작성합니다.
preset.consult.costLabel|4개 역할 · 4개 로그인 · 약 2분 · 낮은 RAM 사용량
preset.coding.displayName|코딩
preset.coding.meta|약 10분
preset.coding.description|구현 작업에 사용합니다. 계획, 검토, 작성, 테스트, 수정 단계를 거쳐 구체적인 최종 결과를 완성합니다.
preset.coding.costLabel|4개 역할 · 4개 로그인 · 8~12분 · 높은 RAM 사용량
preset.roundtable.displayName|원탁회의
preset.roundtable.meta|약 12분
preset.roundtable.description|여러 라운드에 걸쳐 심층적으로 토론합니다. 네 AI가 각각 한 자리씩 맡아 5개 라운드에서 질문을 다시 검토합니다.
preset.roundtable.costLabel|4개 참여 자리 · 4개 로그인 · 10~15분 · 높은 RAM 사용량
preset.brainstorm.displayName|브레인스토밍
preset.brainstorm.meta|12개 라운드 · 48회 발언 · 5개 단계
preset.brainstorm.description|네 AI가 매 라운드 순서를 바꾸어 발언합니다. 문제 설정, 아이디어 확장, 상호 발전, 수집, 선별, 검증 가능한 개념 도출에 걸쳐 총 48회 발언합니다.
preset.brainstorm.costLabel|4개 참여 자리 · 4개 로그인 · 48회 응답 · 45~90분 · 매우 높은 RAM 사용량
preset.readinessAny|{ready}개 연결됨
preset.readinessRequired|{ready}/{total}개 준비됨
connection.sessionReady|백그라운드에서 준비됨
connection.connecting|여는 중…
connection.noWebview|열기
connection.adapterBroken|복구 필요
connection.degraded|연결 문제
connection.needsLogin|로그인
connection.thinking|생각 중
connection.stale|확인 중…
connection.ready|준비됨
connection.readySelected|준비됨 · 선택됨
connection.readyOff|준비됨 · 선택 안 됨
connection.notReady|준비 안 됨
header.exportMarkdown|.md 내보내기
header.maximizeMessages|메시지 패널 최대화
header.restoreMessages|메시지 패널 복원
header.settings|설정
header.followRun|실행 따라가기
header.followRunPaused|따라가기 일시 중지 (수동 포커스)
header.followRunHelp|현재 응답 중인 AI 화면으로 자동 전환합니다.
layout.resizeFocusPane|AI 화면 크기 조절
share.exported|내보내기 완료: {path}
share.exportFailed|이 대화를 내보내지 못했습니다. 다시 시도해 주세요.
provider.access|접근 권한
provider.access.heading|이 어댑터가 접근할 수 있는 항목
provider.access.readTitle|읽기 가능 (페이지에서)
provider.access.writeTitle|쓰기 가능 (페이지에)
provider.access.cannotTitle|접근 불가 (시스템 구조상 보장)
provider.access.replyTitle|AI 답변 텍스트
provider.access.replyDetailWithSelectors|{provider} 페이지에서 어댑터의 응답 선택자와 일치하는 요소의 텍스트를 읽습니다 (대상: AI의 답변).
provider.access.replyDetailGeneric|어댑터의 응답 선택자와 일치하는 페이지 요소의 텍스트를 읽습니다 (대상: AI의 답변).
provider.access.statusTitle|로그인, 로그아웃 및 생각 중 상태
provider.access.statusDetailWithSelectors|{provider}의 어댑터에 정의된 로그인, 로그아웃 및 생각 중 상태 선택자의 존재 여부와 텍스트 일치 여부를 확인합니다.
provider.access.statusDetailGeneric|어댑터에 정의된 로그인, 로그아웃, 생각 중 상태 선택자의 존재 여부와 텍스트 일치 여부를 확인하여 제어 패널에 준비, 로그아웃, 차단 또는 응답 생성 상태를 표시합니다.
provider.access.composerVerifyTitle|입력 후 메시지 작성란의 텍스트
provider.access.composerVerifyDetail|프롬프트 입력 후 작성란의 텍스트를 읽어 정상 입력 여부를 확인하고 필요시 다시 시도합니다.
provider.access.diagnosticsTitle|어댑터 오류 진단
provider.access.diagnosticsDetail|사용자가 직접 신고를 클릭할 때만 어댑터 오류 진단 정보를 읽습니다. 선택자 일치 여부, 허용된 요소 속성, 텍스트 길이만 읽으며 페이지나 메시지의 텍스트 자체는 읽지 않습니다.
provider.access.promptComposerTitle|프롬프트 작성란
provider.access.promptComposerDetailWithSelectors|어댑터 선택자와 일치하는 {provider} 작성란 요소에 프롬프트를 입력합니다.
provider.access.promptComposerDetailGeneric|어댑터가 식별한 {provider} 작성란에 프롬프트를 입력합니다.
provider.access.sendControlTitle|전송 컨트롤
provider.access.sendControlDetailWithSelectors|어댑터 선택자와 일치하는 {provider}의 전송 컨트롤을 클릭합니다.
provider.access.sendControlDetailGeneric|어댑터가 식별한 {provider}의 전송 컨트롤을 클릭합니다.
provider.access.enterFallbackTitle|Enter 키 (대체 방식)
provider.access.enterFallbackDetail|전송 버튼이 없거나 비활성화되어 있거나 어댑터가 Enter 전송 방식을 사용하는 경우 작성란에 Enter 키 이벤트를 보냅니다.
provider.access.stopControlTitle|중지 컨트롤 (사용자가 취소할 때만)
provider.access.stopControlDetail|실행 중인 작업을 취소하기 위해 어댑터에 정의된 중지 버튼을 클릭합니다.
provider.access.cannotCredentialsTitle|쿠키, 비밀번호 및 브라우저 저장소
provider.access.cannotCredentialsDetail|AI 서비스 웹뷰에는 Tauri 권한이 부여되지 않으며 주입된 엔진에는 쿠키, 비밀번호 값 또는 localStorage를 읽는 코드 경로가 없습니다.
provider.access.cannotOtherContextsTitle|다른 탭, 웹뷰, 앱 또는 파일
provider.access.cannotOtherContextsDetail|어댑터는 해당 AI 서비스 웹뷰 안에서만 실행됩니다. 다른 AI 서비스, 브라우저 탭, 창, 파일 또는 데스크톱 앱을 검사할 수 없습니다.
provider.access.cannotRelayTitle|숨겨진 제3자 중계 서버
provider.access.cannotRelayDetail|이 어댑터는 열어 둔 AI 서비스 사이트 이외의 서버로 프롬프트나 답변을 중계하지 않습니다. 해당 AI 서비스는 프롬프트를 받아 답변을 반환합니다. 별도의 숨겨진 제3자 중계 서버는 없습니다. 해당 서비스 외부로 대화 데이터가 나가는 경우는 사용자가 직접 파일로 내보내거나 어댑터 오류 신고를 제출할 때뿐입니다.
provider.access.noSelectorDetails|정확한 선택자 이름은 아직 제어 패널에 표시되지 않습니다. 여기에는 어댑터의 고정된 접근 범위가 표시됩니다.
provider.access.selectorTextIncludes|텍스트에 "{value}" 포함
provider.access.selectorTextExcludes|텍스트에 "{value}" 미포함
provider.realPage|원본 페이지
provider.textView|텍스트
provider.expandStage|확대
provider.collapseStage|복원
provider.center|가운데 정렬
provider.connections|AI 연결
provider.connectionsHint|화면을 전환하거나 연결할 AI를 선택하세요.
provider.currentlyReading|읽는 중
provider.clickToRecover|클릭하여 새로고침하고 연결 복구
provider.login|로그인
provider.metaLoginGuidance|이 창에서 게스트, 이메일/휴대전화 또는 Facebook/Instagram 로그인을 완료하세요. 다른 브라우저에서 로그인하면 이 창으로 돌아올 수 없습니다.
provider.moreActions|AI 서비스 추가 메뉴
provider.reload|새로고침
provider.report|오류 신고
provider.reportFailed|{provider} 오류 신고를 준비하지 못했습니다. 다시 시도해 주세요.
provider.adapterBroken|어댑터 오류
provider.bridgeDegradedReload|브리지 연결이 불안정합니다. 새로고침을 권장합니다.
provider.embeddedLoginBlocked|이 사이트의 보안 검사로 앱 내 로그인이 차단되었습니다. 브라우저에서 이 AI를 사용하거나 나중에 다시 시도하세요.
provider.grokChallengeActive|사이트에서 보안 검사를 진행 중입니다. 이 화면에서 검사를 완료하고 이후에도 상태가 갱신되지 않으면 새로고침하세요.
provider.openInBrowser|브라우저에서 열기
provider.nativeWebviewHidden|네이티브 웹뷰가 숨겨졌지만 백그라운드 작업은 계속됩니다.
provider.nativeWebviewMounted|이 위치에 네이티브 웹뷰가 표시됩니다.
provider.nativeWebviewCentered|네이티브 웹뷰가 가운데에 배치되었습니다.
provider.centerIdle|다음 메시지를 입력할 준비가 되었습니다.
provider.centerReady|준비되었습니다. 아래에 메시지를 입력하세요.
provider.checking|이 AI 세션을 확인하는 중…
provider.signInPrompt|대화를 시작하려면 이 AI에 로그인하세요.
provider.open|열기
provider.opening|여는 중…
provider.openFailed|{provider}을(를) 열지 못했습니다. 다시 시도해 주세요.
provider.retry|다시 시도
onboarding.title|시작할 AI를 선택하세요
onboarding.description|AI를 열고 필요한 경우 한 번 로그인한 뒤 아래에 메시지를 입력하세요.
onboarding.hint|AI 연결 표시줄에서 언제든 다른 AI를 연결할 수 있습니다.
input.workflowRunning|협업 작업 실행 중
input.connectProvider|시작하려면 AI 서비스를 연결하세요
input.sendSelectedProviders|선택한 AI에게 전송
input.messagePlaceholder|메시지 입력… (Enter: 전송, Shift+Enter: 줄바꿈)
input.modeNotReady|이 모드를 사용하려면 AI {remaining}개를 더 연결하세요.
input.preparing|확인 중…
input.preparingSession|새 AI 세션을 준비하는 중…
input.sessionResetFailed|새 AI 세션을 시작하지 못했습니다. 아무 메시지도 전송되지 않았습니다. 다시 시도해 주세요.
input.sendFailed|이 메시지의 처리를 시작하지 못했습니다. 다시 시도해 주세요.
input.reading|읽는 중…
input.insertFile|파일 첨부
input.stop|중지
input.send|전송
input.removeFile|제거
input.bytes|바이트
processTrace.title|실행 과정
processTrace.settled|종료됨
processTrace.waitingEvents|협업 작업 이벤트 대기 중입니다.
processTrace.pending|대기 중
processTrace.active|진행 중
processTrace.done|완료
processTrace.fanout|동시 전송
processTrace.sendingTo|전송 대상:
processTrace.noSelectedAI|선택한 AI 없음
processTrace.response|응답
processTrace.waitingForResponse|응답 대기 중
processTrace.step|단계
workflowStatus.freeTargets|⚡ {providers}에서 동시에 답변 생성 중…
workflowStatus.brainstormTargets|✨ 12개 라운드, 48회 발언으로 구성된 브레인스토밍 시작 중…
workflowStatus.brainstormRound|✨ 브레인스토밍 {round}/12 라운드 · {phase}/5 단계 · {seat}/4 발언자 — {provider} 생각 중…
workflowStatus.consultInitial|🔍 {providers}에서 동시에 답변 생성 중…
workflowStatus.providerStep|{icon} {provider} — {step} 진행 중…
workflowStatus.numberedProviderStep|💻 {number}/{total} 단계 — {provider}: {step}…
workflowStatus.roundtableSpeaker|🔄 {round} 라운드 "{phase}" — {provider} 발언 중…
workflowStatus.nativeEdit|{provider} 작성란에 초안을 입력했습니다. 10분 이내에 해당 AI 화면에서 수정하고 전송하세요.
workflow.providerPageReloaded|응답 도중 {provider} 페이지가 새로고침되어 답변이 사라졌습니다. 해당 단계를 다시 시도하세요.
workflowRole.debate.pro|찬성 논거
workflowRole.debate.con|반대 논거
workflowRole.debate.judge|심사 및 검토
workflowRole.debate.summary|종합
workflowRole.consult.first|초기 답변 A
workflowRole.consult.second|초기 답변 B
workflowRole.consult.reviewer|검토
workflowRole.consult.summary|종합 답변
workflowRole.coding.plannerSpec|명세서 작성
workflowRole.coding.reviewerSpec|명세서 검토
workflowRole.coding.coderV1|초안(v1) 작성
workflowRole.coding.reviewerCode|코드 검토
workflowRole.coding.testerCases|테스트 분석
workflowRole.coding.coderV2|수정본(v2) 작성
workflowRole.coding.plannerAcceptance|인수 검토
workflowRole.coding.coderFinal|최종 수정
workflowRole.brainstorm.round|브레인스토밍 {round} 라운드
workflowRole.roundtable.round|{round} 라운드
workflowRole.roundtable.phase1|초기 입장 제시
workflowRole.roundtable.phase2|상호 검증
workflowRole.roundtable.phase3|심층 토론
workflowRole.roundtable.phase4|핵심 의견 수렴
workflowRole.roundtable.phase5|최종 종합
stepTimeout.waiting|{provider} 응답 대기 중: {seconds}초
stepTimeout.title|단계 제한 시간 초과
stepTimeout.description|{provider}에서 이 협업 단계를 완료하지 못했습니다.
stepTimeout.providerErrorTitle|AI 서비스 단계 실패
stepTimeout.providerErrorDescription|{provider}에서 이 협업 단계를 진행하는 중 오류가 발생했습니다.
stepTimeout.retry|다시 시도
stepTimeout.skip|건너뛰기
stepTimeout.cancel|취소
checkpoint.confirmEachStep|각 단계 전에 확인 요청
checkpoint.sourceInput|출처: 입력 메시지
checkpoint.source|출처:
checkpoint.step|단계
checkpoint.skip|건너뛰기
checkpoint.editInProvider|AI 화면에서 편집
checkpoint.confirm|확인
checkpoint.draftFor|초안 대상:
sessionCheckpoint.interrupted|이전 {mode} 실행이 정상적으로 종료되지 않았습니다.
sessionCheckpoint.step|단계
sessionCheckpoint.pending|대기 중
sessionCheckpoint.replay|다시 실행
sessionCheckpoint.dismiss|닫기
conversation.toggle|대화 목록 열기/닫기
conversation.new|새 대화
conversation.history|대화 기록
conversation.empty|저장된 대화가 없습니다.
conversation.delete|이 대화 삭제
conversation.deleteConfirm|삭제할까요?
settings.title|설정
settings.close|닫기
settings.general|일반
settings.providers|활성 AI 서비스
settings.providersDescription|4개 활성, 1개 대기. 로그인 상태는 유지됩니다.
settings.providersDefault|기본 대기 서비스
settings.providersSelect|대기 AI 서비스
settings.providerActive|활성
settings.providerStandby|대기
settings.modeRoles|협업 역할
settings.modeRolesDescription|기본 구조화 모드는 활성 AI 네 개에 각각 역할을 한 번씩 배정합니다. 역할을 변경할 수 있습니다. 순차 실행 역할에는 동일한 AI를 사용할 수 있지만 자문 모드의 초기 답변 A/B처럼 동시 실행하는 역할은 서로 다른 AI여야 합니다.
settings.modeRoles.coding.planner|기획자
settings.modeRoles.coding.reviewer|검토자
settings.modeRoles.coding.coder|개발자
settings.modeRoles.coding.tester|테스터
settings.modeRoles.roundtable.first|참여자 1
settings.modeRoles.roundtable.second|참여자 2
settings.modeRoles.roundtable.third|참여자 3
settings.modeRoles.roundtable.fourth|참여자 4
settings.privacyHistory|개인정보 및 기록
settings.advanced|고급 설정 및 진단
settings.advancedDescription|어댑터 구성, 접근 권한 상세 정보 및 문제 해결 도구입니다.
settings.madeByTedH|제작: TED-H
settings.sponsoredByAiSister|후원: AI-Sister.com
settings.language|인터페이스 언어
settings.language.system|시스템 기본값
settings.language.en|영어
settings.language.zhTW|중국어(번체)
settings.language.ja|일본어
settings.language.de|독일어
settings.language.ko|한국어
settings.responseLanguage|AI 응답 언어
settings.responseLanguageDescription|질문에 명시된 언어 요청이 항상 우선합니다. 별도 요청이 없으면 자동은 질문과 대화의 언어를 따르고 인터페이스 언어를 대체값으로 사용합니다. 언어를 고정하면 선택한 언어로 답변하도록 요청합니다.
settings.responseLanguage.auto|자동 (권장)
settings.theme|테마
settings.themeLight|밝게
settings.themeDark|어둡게
settings.themeAiSister|AI-Sister 기념 에디션
settings.fontSize|글꼴 크기
theme.aiSister.badge|최종 기념 에디션
theme.aiSister.title|AI-Sister 기념 에디션
theme.aiSister.subtitle|네 목소리, 마지막 한 라운드.
settings.adapterBaseUrl|어댑터 기본 URL
settings.durableSnapshots|스냅샷 영구 저장
settings.durableSnapshotsDescription|기본적으로 꺼져 있습니다. 민감 정보를 가린 후 앱 데이터 폴더에 로컬로 저장합니다. 쿠키나 AI 서비스 저장소는 저장하지 않습니다.
settings.snapshotRedactionTier|스냅샷 정보 보호 수준
settings.snapshotTierMetadataOnly|metadata-only — 구조만 저장, 텍스트 없음. 다시 실행할 때 질문을 다시 입력해야 합니다.
settings.snapshotTierHashes|hashes — SHA-256 해시만 저장하여 내용 비교 가능. 다시 실행할 때 질문을 다시 입력해야 합니다.
settings.snapshotTierPromptText|prompt-text — 질문과 사용자 수정 내용은 평문으로, AI 답변은 해시로 저장합니다.
settings.snapshotTierFullLocal|full-local — 질문과 AI 답변을 이 기기에 평문으로 저장합니다.
settings.updates|업데이트
settings.checking|확인 중…
settings.checkForUpdates|업데이트 확인
settings.upToDate|최신 버전입니다 ({version}).
settings.newVersionAvailable|새 버전 {version}을(를) 사용할 수 있습니다.
settings.downloadPage|다운로드 페이지
settings.downloadPageFailed|다운로드 페이지를 열지 못했습니다. 다시 시도해 주세요.
settings.externalLinkFailed|이 링크를 열지 못했습니다. 다시 시도해 주세요.
settings.releasesUnavailable|릴리스 정보를 확인하지 못했습니다. 나중에 다시 시도하세요.
settings.updateCheckFailed|업데이트 확인 실패:
settings.telemetryNone|텔레메트리: 없음
settings.loading|설정을 불러오는 중…
settings.loadFailed|저장된 설정을 불러오지 못했습니다. 안전한 기본값을 표시합니다.
settings.saveFailed|설정을 저장하지 못했습니다. 다시 시도해 주세요.
settings.technicalDetails|기술 상세 정보
settings.cancel|취소
settings.saved|저장됨
settings.save|저장
settings.diagnostics|진단
settings.diagnosticsDescription|메모리에 보관된 이벤트 로그입니다. 앱을 종료하기 전에 복사하세요.
settings.provider|AI 서비스
settings.all|전체
settings.copied|복사됨
settings.copyFailed|복사 실패
settings.copyLog|로그 복사
settings.exporting|내보내는 중…
settings.exportDebugBundle|디버그 정보 묶음 내보내기
settings.exportCancelled|내보내기가 취소되었습니다.
settings.exportFailed|내보내기 실패:
settings.noEvents|이벤트 없음
settings.bridge|브리지
settings.adapter|어댑터
settings.login|로그인
settings.dom|DOM
settings.thinking|생각 중
settings.webview|웹뷰
settings.yes|예
settings.no|아니요
settings.noDiagnosticEvents|아직 진단 이벤트가 없습니다.
replay.historyToggle|다시 실행 기록
replay.snapshotReplay|스냅샷 다시 실행
replay.description|메모리에 있는 마지막 스냅샷 또는 사용자가 저장한 스냅샷을 일반 협업 작업 방식으로 다시 실행합니다.
replay.lastRun|마지막 작업 다시 실행
replay.noInMemorySnapshot|아직 메모리에 저장된 스냅샷이 없습니다.
replay.storedSnapshots|저장된 스냅샷
replay.durableSnapshotsOptIn|스냅샷 영구 저장은 설정에서 직접 활성화할 수 있습니다.
replay.refresh|새로고침
replay.loadingStoredSnapshots|저장된 스냅샷을 불러오는 중…
replay.noStoredSnapshots|저장된 스냅샷이 없습니다. 재시작 후에도 다시 실행 기록을 유지하려면 설정에서 스냅샷 영구 저장을 켜세요.
replay.unknownGraph|알 수 없는 작업 그래프
replay.createdTimeUnknown|생성 시간 알 수 없음
replay.replay|다시 실행
replay.delete|삭제
replay.originalQuestionRequired|원래 질문 필요
replay.originalQuestionDescription|이 스냅샷에는 원래 프롬프트가 저장되지 않았습니다. {source}을(를) 다시 실행하려면 질문을 입력하세요.
replay.originalQuestion|원래 질문
replay.graphVersionChanged|작업 그래프 버전 변경됨
replay.graphVersionMismatch|스냅샷 버전 {snapshotVersion}이(가) 현재 버전 {currentVersion}과(와) 일치하지 않습니다.
replay.replayWithCurrentGraph|현재 작업 그래프로 다시 실행
replay.cannotStartReplay|다시 실행할 수 없음
replay.preflightHelp|사용할 수 없는 AI 서비스를 열거나 로그인한 후 다시 실행하세요.
replay.unavailable|사용할 수 없음
replay.openLogin|열기/로그인
replay.aliasedRoles|중복 배정된 역할:
replay.snapshotNotFound|스냅샷을 찾을 수 없습니다.
replay.snapshotGraphUnavailable|스냅샷의 작업 그래프를 사용할 수 없습니다.
replay.blocked|다시 실행 차단됨:
replay.completed|다시 실행을 완료했습니다.
replay.completedWithSnapshot|다시 실행 완료: {snapshotId}
replay.snapshotDeleted|스냅샷을 삭제했습니다.
replay.sourceLastRun|마지막 작업
preflight.cannotStart|다음 AI 서비스를 사용할 수 없어 {mode} 모드를 시작할 수 없습니다.
preflight.noWebview|웹뷰 없음
preflight.needsLogin|로그인 필요
preflight.stale|상태 갱신 필요
preflight.unavailable|사용할 수 없음
preflight.aliasedProvider|두 역할에 동일한 AI 서비스가 배정됨
preflight.openLogin|열기/로그인
preflight.reassignRole|역할 재배정
preflight.close|뒤로
preflight.switchMode|동시 질문 모드 사용
reportPreview.title|오류 신고 미리보기
reportPreview.provider|AI 서비스
reportPreview.adapterVersion|어댑터 버전
reportPreview.appVersion|앱 버전
reportPreview.path|경로
reportPreview.firstMissingField|조치가 필요한 선택자 오류
reportPreview.none|없음
reportPreview.noStructuralFailure|구조적인 선택자 오류가 감지되지 않았습니다. 빈 작성란에는 전송 버튼이 나타나지 않고 새 대화에는 응답 노드가 없습니다. 실제 오류를 재현하고 디버그 로그를 내보낸 뒤 이슈를 등록하세요.
reportPreview.cancel|취소
reportPreview.openGithubIssue|GitHub 이슈 열기
reportPreview.openFailed|GitHub 이슈를 열지 못했습니다. 다시 시도해 주세요.
fileInsert.binaryUnsupported|PDF, 이미지 및 문서 파일은 아직 지원하지 않습니다. 일반 텍스트 파일을 선택하세요.
fileInsert.fileTooLarge|텍스트 파일은 약 256KB보다 작아야 합니다. 더 작은 파일을 선택하세요.
fileInsert.attachmentLimit|총 용량 약 256KB 이내로 최대 8개의 텍스트 파일을 첨부할 수 있습니다. 파일을 제거하거나 더 작은 파일을 선택하세요.
chat.noMessages|아직 메시지가 없습니다.
chat.noProviders|왼쪽에서 AI를 열고 로그인하여 대화를 시작하세요.
chat.readyPrompt|모드를 선택한 뒤 아래에 메시지를 입력하세요.
chat.streaming|응답 생성 중
chat.thinking|생각 중…
chat.truncated|(일부 생략됨)
fatal.title|앱에서 예상치 못한 문제가 발생했습니다.
fatal.description|AI 세션은 로컬에 저장되어 있습니다. 계속하려면 제어 패널을 새로고침하세요.
fatal.reload|앱 새로고침
'''

EXPECTED_COUNT = 361
EXPECTED_KEY_HASH = 309150764
NEW_KEY = 'settings.language.ko'
ENTRY_RE = re.compile(r"^\s*'([^']+)':\s*(['\"])((?:\\.|(?!\2)[\s\S])*?)\2,\s*$", re.M)
PLACEHOLDER_RE = re.compile(r'\{\w+\}')


def assert_condition(condition, message):
    if not condition:
        raise ValueError(message)


def load_translations():
    translations = {}
    for line in TRANSLATIONS.strip().splitlines():
        key, val = line.split('|', 1)
        assert_condition(key not in translations and val.strip(), f'Invalid or duplicate translation: {key}')
        translations[key] = val
    return translations


def key_hash(keys):
    value = 0
    for ch in '\n'.join(sorted(keys)):
        value = (value * 31 + ord(ch)) & 0xffffffff
    return value


def entries(source):
    matches = ENTRY_RE.findall(source)
    result = {key: val for key, _, val in matches}
    assert_condition(len(matches) == len(result), 'Duplicate keys in source dictionary')
    return result


def replace_exact(source, old, new, path, count=1):
    actual = source.count(old)
    assert_condition(actual == count, f'{path}: expected {count} matches, found {actual}: {old[:120]}')
    return source.replace(old, new)


def quote(value):
    return "'" + value.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n') + "'"


def plan(root):
    translations = load_translations()
    base_keys = set(translations) - {NEW_KEY}
    assert_condition(len(base_keys) == EXPECTED_COUNT and key_hash(base_keys) == EXPECTED_KEY_HASH,
                     'The bundled translations do not match the audited upstream key set')
    assert_condition((root / 'package.json').is_file(), 'Run this script in the repository root or supply its path.')
    package = json.loads((root / 'package.json').read_text(encoding='utf-8'))
    assert_condition(package.get('name') == 'multi-ai-chat-desktop', 'This is not Multi-AI Chat Desktop.')
    changes = {}
    originals = {}

    def read(path):
        if path not in originals:
            originals[path] = (root / path).read_text(encoding='utf-8')
        return changes.get(path, originals[path])

    def edit(path, old, new, count=1):
        changes[path] = replace_exact(read(path), old, new, path, count)

    en_path = 'src/i18n/en.ts'
    english = entries(read(en_path))
    missing = set(english) - base_keys
    extra = base_keys - set(english)
    assert_condition(not missing and not extra,
                     f'Upstream dictionary differs from this patch. Missing translations: {sorted(missing)}; extra: {sorted(extra)}')
    for key, value in english.items():
        assert_condition(sorted(PLACEHOLDER_RE.findall(value)) == sorted(PLACEHOLDER_RE.findall(translations[key])),
                         f'Placeholder mismatch: {key}')
    ko_path = 'src/i18n/ko.ts'
    assert_condition(not (root / ko_path).exists(), f'{ko_path} already exists; refusing to overwrite.')
    key_path = 'src/i18n/keys.ts'
    edit(key_path, "  'settings.language.de',", "  'settings.language.de',\n  'settings.language.ko',")
    for lang, label in [('en', 'Korean'), ('de', 'Koreanisch'), ('ja', '\u97d3\u56fd\u8a9e'), ('zh-TW', '\u97d3\u6587')]:
        path = f'src/i18n/{lang}.ts'
        source = read(path)
        assert_condition(set(entries(source)) == base_keys, f'{path}: upstream dictionary key set differs')
        lines = re.findall(r"^  'settings\.language\.de':[^\n]+$", source, re.M)
        assert_condition(len(lines) == 1, f'{path}: could not locate language option')
        edit(path, lines[0], lines[0] + f"\n  'settings.language.ko': {quote(label)},")
    ko = ["import type { I18nKey } from './keys';", '', 'export const ko: Record<I18nKey, string> = {']
    for key in english:
        ko.append(f'  {quote(key)}: {quote(translations[key])},')
        if key == 'settings.language.de':
            ko.append(f'  {quote(NEW_KEY)}: {quote(translations[NEW_KEY])},')
    ko += ['};', '']
    changes[ko_path] = '\n'.join(ko)

    path = 'src/i18n/resolve.ts'
    edit(path, "export type LanguageSetting = 'system' | 'en' | 'zh-TW' | 'ja' | 'de';",
         "export type LanguageSetting = 'system' | 'en' | 'zh-TW' | 'ja' | 'de' | 'ko';")
    edit(path, "['system', 'en', 'zh-TW', 'ja', 'de']", "['system', 'en', 'zh-TW', 'ja', 'de', 'ko']")
    edit(path, "['auto', 'en', 'zh-TW', 'ja', 'de']", "['auto', 'en', 'zh-TW', 'ja', 'de', 'ko']")
    edit(path, "  if (normalized === 'en' || normalized.startsWith('en-')) return 'en';",
         "  if (normalized === 'ko' || normalized.startsWith('ko-')) return 'ko';\n  if (normalized === 'en' || normalized.startsWith('en-')) return 'en';")

    path = 'src/i18n/t.ts'
    edit(path, "import { ja } from './ja';", "import { ja } from './ja';\nimport { ko } from './ko';")
    edit(path, '  de,\n};', '  de,\n  ko,\n};')

    path = 'src/ui/SettingsModal.tsx'
    option = '<option value="de">{t(\'settings.language.de\')}</option>'
    edit(path, option, option + '\n                  <option value="ko">{t(\'settings.language.ko\')}</option>', count=2)

    path = 'src/workflow/responseLanguage.ts'
    edit(path, "  de: 'German (de)',", "  de: 'German (de)',\n  ko: 'Korean (ko)',")
    edit(path, "new Set<Locale>(['en', 'zh-TW', 'ja', 'de'])", "new Set<Locale>(['en', 'zh-TW', 'ja', 'de', 'ko'])")

    path = 'src/workflow/graph/registries.ts'
    edit(path, "  if (locale === 'ja') return filtered.join('\u3001');",
         "  if (locale === 'ja') return filtered.join('\u3001');\n  if (locale === 'ko') return filtered.join(', ');")

    path = 'src-tauri/src/settings.rs'
    edit(path, 'const LANGUAGES: &[&str] = &["system", "en", "zh-TW", "ja", "de"];',
         'const LANGUAGES: &[&str] = &["system", "en", "zh-TW", "ja", "de", "ko"];')
    edit(path, 'const RESPONSE_LANGUAGES: &[&str] = &["auto", "en", "zh-TW", "ja", "de"];',
         'const RESPONSE_LANGUAGES: &[&str] = &["auto", "en", "zh-TW", "ja", "de", "ko"];')
    edit(path, '        for language in ["auto", "en", "zh-TW", "ja", "de"] {',
         '        for language in ["auto", "en", "zh-TW", "ja", "de", "ko"] {')
    old = '    fn normalizes_language_setting_to_supported_values() {'
    edit(path, old, old + '\n        assert_eq!(\n            normalize_settings_value(json!({ "language": "ko" })).get("language"),\n            Some(&json!("ko"))\n        );')

    path = 'src/__tests__/i18n.test.ts'
    edit(path, "import { ja } from '../i18n/ja';", "import { ja } from '../i18n/ja';\nimport { ko } from '../i18n/ko';")
    edit(path, "const dictionaries = { en, 'zh-TW': zhTW, ja, de } as const;",
         "const dictionaries = { en, 'zh-TW': zhTW, ja, de, ko } as const;")
    edit(path, "expect(LANGUAGE_SETTINGS).toEqual(['system', 'en', 'zh-TW', 'ja', 'de']);",
         "expect(LANGUAGE_SETTINGS).toEqual(['system', 'en', 'zh-TW', 'ja', 'de', 'ko']);\n    expect(normalizeLanguageSetting('ko')).toBe('ko');")
    edit(path, "expect(RESPONSE_LANGUAGE_SETTINGS).toEqual(['auto', 'en', 'zh-TW', 'ja', 'de']);",
         "expect(RESPONSE_LANGUAGE_SETTINGS).toEqual(['auto', 'en', 'zh-TW', 'ja', 'de', 'ko']);\n    expect(normalizeResponseLanguageSetting('ko')).toBe('ko');")
    edit(path, "expect(resolveLocale('system', ['de-DE'])).toBe('de');",
         "expect(resolveLocale('system', ['de-DE'])).toBe('de');\n    expect(resolveLocale('system', ['ko'])).toBe('ko');\n    expect(resolveLocale('system', ['ko-KR'])).toBe('ko');\n    expect(resolveLocale('system', ['KO_kr'])).toBe('ko');\n    expect(resolveLocale('system', ['fr-FR', 'ko-KR', 'en-US'])).toBe('ko');")
    edit(path, "expect(resolveLocale('de', ['ja-JP'])).toBe('de');",
         "expect(resolveLocale('de', ['ja-JP'])).toBe('de');\n    expect(resolveLocale('ko', ['en-US'])).toBe('ko');")

    path = 'src/__tests__/responseLanguage.test.ts'
    anchor = "describe('response language policy', () => {"
    edit(path, anchor, anchor + "\n  it('supports Korean as a fixed response language and interface fallback', () => {\n    const policy = createResponseLanguagePolicy('ko', 'ko');\n    expect(isResponseLanguagePolicy(policy)).toBe(true);\n    expect(responseLanguageDirective(policy)).toContain('Korean (ko)');\n    expect(responseLanguagePolicyFromPrompt(prependResponseLanguagePolicy('question', policy))).toEqual(policy);\n    expect(responseLanguageDirective(createResponseLanguagePolicy('auto', 'ko'))).toContain('Korean (ko) (the app interface language fallback)');\n  });\n")

    # Validate all five final dictionaries, including substitution parameters.
    for lang in ['en', 'de', 'ja', 'zh-TW', 'ko']:
        data = entries(changes[f'src/i18n/{lang}.ts'])
        assert_condition(set(data) == set(translations), f'Final dictionary key mismatch: {lang}')
        for key, value in data.items():
            assert_condition(value.strip() and sorted(PLACEHOLDER_RE.findall(value)) == sorted(PLACEHOLDER_RE.findall(translations[key])),
                             f'Final dictionary placeholder mismatch: {lang}/{key}')
    return originals, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', nargs='?', default='.', help='Path to the cloned repository')
    parser.add_argument('--check', action='store_true', help='Validate patch anchors and dictionaries without changing files')
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    try:
        originals, changes = plan(root)
    except (OSError, ValueError, KeyError) as exc:
        print(f'Patch not applied: {exc}', file=sys.stderr)
        return 1
    print(f'Validated {len(load_translations())} Korean translation keys and placeholders.')
    print('Files to change:')
    for path in changes:
        print('  ' + path)
    if args.check:
        print('Check passed. No files were changed.')
        return 0
    # All expected anchors are checked before any write. Roll back if a write fails.
    written = []
    backups = {p: (root / p).read_bytes() for p in originals if p in changes}
    try:
        for path, source in changes.items():
            written.append(path)
            (root / path).write_text(source, encoding='utf-8', newline='\n')
    except OSError as exc:
        for path in reversed(written):
            file = root / path
            if path in backups:
                file.write_bytes(backups[path])
            else:
                file.unlink(missing_ok=True)
        print(f'Patch write failed, attempted rollback: {exc}', file=sys.stderr)
        return 1
    print('Korean source patch applied. Review git diff, run pnpm verify, then build.')
    print('No GitHub upload or binary build has been performed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
