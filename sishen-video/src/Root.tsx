import React from "react";
import { Composition, Folder } from "remotion";
import { SishenLove, SCENES, TOTAL } from "./SishenLove";
import { FaceTest } from "./FaceTest";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="SishenLove" component={SishenLove} width={1920} height={1080} fps={30} durationInFrames={TOTAL} />
    <Composition id="FaceTest" component={FaceTest} width={1920} height={1080} fps={30} durationInFrames={1} defaultProps={{ name: "fuling_idle" }} />
    <Folder name="Scenes">
      {SCENES.map(({ id, C, d }) => (
        <Composition key={id} id={id} component={C} width={1920} height={1080} fps={30} durationInFrames={d} />
      ))}
    </Folder>
  </>
);
