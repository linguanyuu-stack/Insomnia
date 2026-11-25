import React from "react";
import { Composition, Folder } from "remotion";
import { SishenLove, SCENES, TOTAL } from "./SishenLove";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="SishenLove" component={SishenLove} width={1920} height={1080} fps={30} durationInFrames={TOTAL} />
    <Folder name="Scenes">
      {SCENES.map(({ id, C, d }) => (
        <Composition key={id} id={id} component={C} width={1920} height={1080} fps={30} durationInFrames={d} />
      ))}
    </Folder>
  </>
);
