
export type Owner = number;
export type MeOwner = Owner;
export type OpponentOwner = Owner;

export interface Cell {
  /**
   * cell position
   */
  position: {
    x: number,
    y: number,
  },
  /**
   * neighbours by direction of the cell
   */
  neighbours: {
    /**
     * horizontal neighbours
     */
    horizontal: [MeOwner, OpponentOwner],
    /**
     * vertical neighbours
     */
    vertical: [MeOwner, OpponentOwner],
    /**
     * diagonal from top left corner to bottom right corner
     */
    leftCorner: [MeOwner, OpponentOwner],
    /**
     * diagonal from top right corner to bottom left corner
     */
    rightCorner: [MeOwner, OpponentOwner],
  },
  /**
   * is cell is free ?
   */
  isFree: boolean,
  /**
   * the weight of the cell, higher the weight is best is.
   */
  weight: number,
  /**
   * the owner of the cell
   */
  owner: number,
};
